import importlib.util
from pathlib import Path
import sys
import unittest
import os
from unittest.mock import patch
from tempfile import TemporaryDirectory
import base64

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

    def test_svg_output(self):
        svg = b'<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0h1"/></svg>'
        with TemporaryDirectory() as directory:
            path = Path(directory) / 'icon.svg'
            for payload in (b'not XML', b'<html/>'):
                with self.assertRaises(cli.CliError):
                    cli.write_images([(base64.b64encode(payload).decode(), None)], str(path), 'svg')
                self.assertFalse(path.exists())
            cli.write_images([(base64.b64encode(svg).decode(), None)], str(path), 'svg')
            self.assertEqual(path.read_bytes(), svg)

    def test_format_constraints(self):
        for flags in (('--output-format', 'svg', '--count', '2'), ('--frame-count', '2'),
                      ('--markup', 'overlay.png'), ('--size', '1000x1000'),
                      ('--background', 'transparent', '--output-format', 'jpg'),
                      ('--output-format', 'gif', '--frame-count', '17')):
            with self.subTest(flags=flags), self.assertRaises(cli.CliError):
                self.body(*flags)
        body = self.body('--output-format', 'gif', '--size', '512x512', '--frame-count', '4')
        self.assertEqual(body['frame_count'], 4)
        self.assertNotIn('output_compression', body)


if __name__ == '__main__':
    unittest.main()
