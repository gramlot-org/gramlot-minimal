import argparse
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from fixture_provider import DECLARATIONS, compile_project as fixture_compile
from gramlot_standalone.cli import main, run_build
from gramlot_standalone.errors import ProviderError
from gramlot_standalone.html import build_html
from gramlot_standalone.project import Project
from gramlot_standalone.provider import compile_project, validate_result

class ProviderHtmlCliTests(unittest.TestCase):
    def make_project(self, root):
        (root/"pages").mkdir(); (root/"pages"/"index.py").write_text("# fixture\n")
        (root/"pages"/"other.py").write_text("# fixture two\n")
        return Project.load(root)

    def test_missing_provider_fails_without_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); self.make_project(root); output=root/"site.html"
            with patch("gramlot_standalone.provider.importlib.import_module", side_effect=ModuleNotFoundError("gramlot")):
                self.assertEqual(main(["build", str(root), "-o", str(output)]), 2)
            self.assertFalse(output.exists())

    def test_remote_css_fails_before_provider_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); self.make_project(root)
            (root/"style.css").write_text("body{background:url(https://example.test/x)}")
            output=root/"site.html"
            self.assertEqual(main(["build", str(root), "-o", str(output),
                                   "--provider", "fixture_provider:compile_project"]), 2)
            self.assertFalse(output.exists())

    def test_requires_complete_profile_and_finite_json(self):
        with tempfile.TemporaryDirectory() as directory:
            project=self.make_project(Path(directory)); response=fixture_compile(project.request())
            response["capability_declarations"] = DECLARATIONS[:-1]
            with self.assertRaisesRegex(ProviderError, "download-updated-html-v1"):
                validate_result(project, response)
            response=fixture_compile(project.request()); response["pages"][0]["source"]={"x":float("nan")}
            with self.assertRaisesRegex(ProviderError, "finite JSON"):
                validate_result(project, response)

    def test_rejects_output_receipt_collision_without_write(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); self.make_project(root); output=root/"site.html"
            args=argparse.Namespace(source=str(root), output=str(output),
                provider="fixture_provider:compile_project", build_info=str(output), command="build")
            with self.assertRaisesRegex(Exception, "different paths"):
                run_build(args)
            self.assertFalse(output.exists())

    def test_html_is_deterministic_safe_and_cli_atomic(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); project=self.make_project(root)
            compiled=compile_project(project, fixture_compile)
            first, info1=build_html(project, compiled); second, info2=build_html(project, compiled)
            self.assertEqual((first, info1), (second, info2))
            self.assertIn("connect-src 'none'", first)
            self.assertNotIn("</ScRiPt><img", first)
            self.assertIn("\\u003c/script>", first)
            self.assertNotIn("<\\/script><img", first)
            self.assertNotIn("<script src=", first)
            output=root/"out"/"site.html"; receipt=root/"out"/"build.json"
            args=argparse.Namespace(source=str(root), output=str(output),
                provider="fixture_provider:compile_project", build_info=str(receipt), command="build")
            info=run_build(args)
            self.assertEqual(output.read_text(), first)
            self.assertEqual(json.loads(receipt.read_text())["sha256"], info["sha256"])
            self.assertFalse(any(output.parent.glob(".site.html.*")))

if __name__ == "__main__": unittest.main()
