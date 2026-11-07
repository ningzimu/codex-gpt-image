import importlib.util
from pathlib import Path
import sys
import unittest
import os
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/codex-gpt-image/scripts/codex_gpt_image.py'
spec = importlib.util.spec_from_file_location('codex_gpt_image', SCRIPT)
cli = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = cli
spec.loader.exec_module(cli)


class ImageParametersTest(unittest.TestCase):
    def body(self, *flags):
        args = cli.build_parser().parse_args(['generate', '--prompt', 'test', *flags])
        return cli.build_image_body(args, 'test', [])[2]

    def test_latest_models(self):
        self.assertEqual(self.body()['model'], 'gpt-image-2.6-flare')
        for model in cli.SUPPORTED_MODELS:
            body = self.body('--model', model, '--quality', 'max', '--size', '1536x864',
                             '--complexity', 'medium', '--background', 'transparent')
            self.assertEqual(body['complexity'], 'medium')
            self.assertEqual(body['model'], model)

    def test_reject_other_models(self):
        for model in ('gpt-image-2', 'gpt-image-2.5-flare', 'gpt-image-2.6-flare-invalid'):
            with self.subTest(model=model), patch.dict(os.environ, CODEX_GPT_IMAGE_MODEL=model):
                with self.assertRaises(cli.CliError):
                    self.body()

    def test_size_boundaries(self):
        for size in ('auto', '1024x640', '3840x2160'):
            self.body('--size', size)
        for size in ('1000x1000', '4096x2048', '1024x512', '3840x1024', '3840x3840'):
            with self.subTest(size=size), self.assertRaises(cli.CliError):
                self.body('--size', size)

    def test_format_constraints(self):
        for flags in (('--markup', 'overlay.png'),
                      ('--background', 'transparent', '--output-format', 'jpg')):
            with self.subTest(flags=flags), self.assertRaises(cli.CliError):
                self.body(*flags)
        for fmt in ('svg', 'gif'):
            with self.subTest(fmt=fmt), self.assertRaises(cli.CliError):
                cli.normalize_output_format(fmt)


if __name__ == '__main__':
    unittest.main()
