import importlib.util
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/codex-gpt-image/scripts/codex_gpt_image.py'
spec = importlib.util.spec_from_file_location('codex_gpt_image', SCRIPT)
cli = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = cli
spec.loader.exec_module(cli)


class ImageParametersTest(unittest.TestCase):
    def body(self, *flags):
        args = cli.build_parser().parse_args(['generate', '--prompt', 'test', *flags])
        return cli.build_image_body(args.prompt, args.image or [], args.transparent_background)

    def test_optional_fields_are_absent_by_default(self):
        self.assertEqual(self.body(), {'prompt': 'test'})

    def test_transparency_is_opt_in(self):
        self.assertEqual(self.body('--transparent-background'),
                         {'prompt': 'test', 'background': 'transparent'})

    def test_references_preserve_order_and_allow_optional_transparency(self):
        with patch.object(cli, 'image_reference', side_effect=lambda path: path.name):
            for flags in ([], ['--transparent-background']):
                with self.subTest(flags=flags):
                    body = self.body('-i', 'first.png', '-i', 'second.png', *flags)
                    expected = {'prompt': 'test', 'images': ['first.png', 'second.png']}
                    if flags:
                        expected['background'] = 'transparent'
                    self.assertEqual(body, expected)


if __name__ == '__main__':
    unittest.main()
