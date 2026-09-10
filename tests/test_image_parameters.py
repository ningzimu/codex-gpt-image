import importlib.util
from pathlib import Path
import sys
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/codex-gpt-image/scripts/codex_gpt_image.py'
spec = importlib.util.spec_from_file_location('codex_gpt_image', SCRIPT)
cli = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = cli
spec.loader.exec_module(cli)


class ImageParametersTest(unittest.TestCase):
    def body(self, *flags):
        args = cli.build_parser().parse_args(['generate', '--prompt', 'test', *flags])
        return cli.build_image_body(args, 'test', [])[2]

    def test_default_model_and_legacy_override(self):
        self.assertEqual(self.body()['model'], 'gpt-image-2.5-flare')
        self.assertEqual(self.body('--model', 'gpt-image-2')['model'], 'gpt-image-2')

    def test_new_models_and_snapshots_accept_new_options(self):
        for model in ('gpt-image-2.5-flare', 'gpt-image-2.5-sunburst'):
            for suffix in ('', '-2026-09-08'):
                for quality in ('xhigh', 'max'):
                    for fmt in ('png', 'webp'):
                        with self.subTest(model=model + suffix, quality=quality, fmt=fmt):
                            body = self.body('--model', model + suffix, '--quality', quality,
                                             '--background', 'transparent', '--output-format', fmt)
                            self.assertEqual(body['quality'], quality)
                            self.assertEqual(body['background'], 'transparent')

    def test_legacy_rejects_new_options(self):
        for model in ('gpt-image-2', 'gpt-image-2-2026-04-21'):
            for option in (('--quality', 'max'), ('--quality', 'xhigh'), ('--background', 'transparent')):
                with self.subTest(model=model, option=option), self.assertRaises(cli.CliError):
                    self.body('--model', model, *option)

    def test_transparent_jpeg_rejected(self):
        for fmt in ('jpeg', 'jpg'):
            with self.subTest(fmt=fmt), self.assertRaises(cli.CliError):
                self.body('--background', 'transparent', '--output-format', fmt)

    def test_size_boundaries(self):
        for model in ('gpt-image-2', 'gpt-image-2.5-flare', 'gpt-image-2.5-sunburst'):
            for size in ('auto', '1024x640', '3840x2160'):
                with self.subTest(model=model, size=size):
                    self.body('--model', model, '--size', size)
            for size in ('1000x1000', '4096x2048', '1024x512', '3840x1024', '3840x3840'):
                with self.subTest(model=model, size=size), self.assertRaises(cli.CliError):
                    self.body('--model', model, '--size', size)

    def test_model_matching_is_not_substring_based(self):
        for model in ('not-gpt-image-2', 'gpt-image-20', 'gpt-image-2.5-flare-invalid'):
            self.assertFalse(cli.is_gpt_image_2(model))
            self.assertFalse(cli.is_gpt_image_2_5(model))


if __name__ == '__main__':
    unittest.main()
