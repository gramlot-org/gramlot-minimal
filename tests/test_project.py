import os
from pathlib import Path
import tempfile
import unittest
from gramlot_standalone.errors import ProjectError
from gramlot_standalone.project import Project

class ProjectTests(unittest.TestCase):
    def make_project(self, root):
        (root / "pages").mkdir()
        (root / "pages" / "home.py").write_text("# page\n", encoding="utf-8")
        (root / "pages" / "index.py").write_text("# index\n", encoding="utf-8")

    def test_discovers_index_config_css_resource_and_preserves_fragment(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); self.make_project(root)
            (root/"resources").mkdir(); (root/"resources"/"sprite.svg").write_text("<svg/>")
            (root/"style.css").write_text(".icon{background:url(resources/sprite.svg#mark)}")
            project=Project.load(root)
            self.assertEqual([p.slug for p in project.pages], ["home", "index"])
            self.assertEqual(project.initial_page, "index")
            self.assertIn("data:image/svg+xml;base64,", project.css)
            self.assertIn("#mark", project.css)

    def test_rejects_remote_import_escape_and_missing_resource(self):
        cases = [
            ("body{background:url(https://example.test/x)}", "Remote CSS"),
            ('@import "theme.css";', "@import"),
            ('body{content:"\\41"}', "CSS escapes"),
            ("body{background:url(../outside.png)}", "escapes project"),
            ("body{background:url(resources/x.png?v=1)}", "query strings"),
            ("body{background:url(missing.png)}", "under resources"),
        ]
        for css, message in cases:
            with self.subTest(css=css), tempfile.TemporaryDirectory() as directory:
                root=Path(directory); self.make_project(root); (root/"style.css").write_text(css)
                with self.assertRaisesRegex(ProjectError, message): Project.load(root)

    def test_rejects_input_symlinks_that_escape(self):
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            root=Path(directory); external=Path(outside); (external/"pages").mkdir()
            (external/"pages"/"home.py").write_text("# external\n")
            os.symlink(external/"pages", root/"pages")
            with self.assertRaisesRegex(ProjectError, "escapes"):
                Project.load(root)
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            root=Path(directory); self.make_project(root); external=Path(outside)/"secret.bin"
            external.write_bytes(b"secret"); (root/"resources").mkdir()
            os.symlink(external, root/"resources"/"secret.bin")
            with self.assertRaisesRegex(ProjectError, "escapes"):
                Project.load(root)

    def test_stylesheet_filename_is_not_interpolated_into_css(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); self.make_project(root)
            weird=root/"styles"/"evil*"; weird.mkdir(parents=True)
            (weird/"safe.css").write_text("body{color:black}")
            project=Project.load(root)
            self.assertNotIn("evil", project.css)
            self.assertEqual(project.css.strip(), "body{color:black}")

    def test_rejects_non_string_initial_page(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); self.make_project(root)
            (root/"gramlot-standalone.toml").write_text("[site]\ninitial_page=[]\n")
            with self.assertRaisesRegex(ProjectError, "page slug"):
                Project.load(root)

if __name__ == "__main__": unittest.main()
