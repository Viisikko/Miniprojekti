import unittest
from unittest.mock import patch

import generate_bibtex


class TestRowToBibtex(unittest.TestCase):
    def test_basic_article(self):
        row = {
            "id": 1,
            "type": "article",
            "index": "Turing1950",
            "year": 1950,
            "title": "Computing Machinery and Intelligence",
            "author": ["Alan Turing"],
            "journal": "Mind",
            "doi": "10.1093/mind/LIX.236.433",
        }

        bib = generate_bibtex.row_to_bibtex(row)

        self.assertIn("@article{Turing1950,", bib)
        self.assertIn("author = {Alan Turing}", bib)
        self.assertIn("title = {Computing Machinery and Intelligence}", bib)
        self.assertIn("year = {1950}", bib)
        self.assertIn("journal = {Mind}", bib)
        self.assertIn("doi = {10.1093/mind/LIX.236.433}", bib)
        self.assertTrue(bib.strip().endswith("}"))

    def test_multiple_authors(self):
        row = {
            "id": 2,
            "type": "book",
            "index": "Doe2020",
            "year": 2020,
            "title": "Test Book",
            "author": ["John Doe", "Jane Roe"],
            "publisher": "Test Publisher",
        }

        bib = generate_bibtex.row_to_bibtex(row)

        self.assertIn("@book{Doe2020,", bib)
        self.assertIn("author = {John Doe and Jane Roe}", bib)
        self.assertIn("publisher = {Test Publisher}", bib)

    def test_brace_escaping(self):
        row = {
            "id": 3,
            "type": "misc",
            "index": "WeirdTitle2024",
            "year": 2024,
            "title": "A {weird} title with {braces}",
            "author": ["Some One"],
        }

        bib = generate_bibtex.row_to_bibtex(row)

        self.assertIn(
            "title = {A \\{weird\\} title with \\{braces\\}}",
            bib,
        )


class TestExportViitteetToBibtex(unittest.TestCase):
    @patch("generate_bibtex.query")
    def test_export_without_references_list(self, mock_query):
        """Test export when no references_list is provided - should query database"""
        mock_query.return_value = [
            {
                "id": 1,
                "type": "article",
                "index": "A1",
                "year": 2000,
                "title": "First",
                "author": ["Alice"],
            },
            {
                "id": 2,
                "type": "book",
                "index": "B2",
                "year": 2010,
                "title": "Second",
                "author": ["Bob"],
            },
        ]

        content = generate_bibtex.export_viitteet_to_bibtex()

        mock_query.assert_called_once_with(
            "SELECT * FROM viitteet ORDER BY id",
            {},
        )

        entries = [e for e in content.strip().split("\n\n") if e.strip()]
        self.assertEqual(len(entries), 2)
        self.assertIn("@article{A1,", content)
        self.assertIn("@book{B2,", content)

    @patch("generate_bibtex.query")
    def test_export_with_references_list(self, mock_query):
        """Test export when references_list is provided - should not query database"""
        references_list = [
            {
                "id": 3,
                "type": "article",
                "index": "Filtered1",
                "year": 2022,
                "title": "Filtered Article",
                "author": ["Jane Smith"],
                "journal": "Science",
            },
        ]

        content = generate_bibtex.export_viitteet_to_bibtex(references_list)

        # Should NOT call query since we provided a list
        mock_query.assert_not_called()

        self.assertIn("@article{Filtered1,", content)
        self.assertIn("author = {Jane Smith}", content)
        self.assertIn("journal = {Science}", content)

    @patch("generate_bibtex.query")
    def test_export_with_empty_references_list(self, mock_query):
        """Test export with empty references_list returns empty content"""
        content = generate_bibtex.export_viitteet_to_bibtex([])

        # Should NOT call query
        mock_query.assert_not_called()

        self.assertIn(content, ("", "\n"))

    @patch("generate_bibtex.query")
    def test_export_with_filtered_references(self, mock_query):
        """Test export with multiple filtered references"""
        filtered_refs = [
            {
                "id": 10,
                "type": "book",
                "index": "Smith2020",
                "year": 2020,
                "title": "Python Programming",
                "author": ["John Smith", "Alice Brown"],
                "publisher": "Tech Books",
            },
            {
                "id": 15,
                "type": "article",
                "index": "Doe2021",
                "year": 2021,
                "title": "AI Research",
                "author": ["Jane Doe"],
                "doi": "10.1234/ai.2021",
            },
        ]

        content = generate_bibtex.export_viitteet_to_bibtex(filtered_refs)

        mock_query.assert_not_called()

        entries = [e for e in content.strip().split("\n\n") if e.strip()]
        self.assertEqual(len(entries), 2)
        self.assertIn("@book{Smith2020,", content)
        self.assertIn("author = {John Smith and Alice Brown}", content)
        self.assertIn("@article{Doe2021,", content)
        self.assertIn("doi = {10.1234/ai.2021}", content)


if __name__ == "__main__":
    unittest.main()
