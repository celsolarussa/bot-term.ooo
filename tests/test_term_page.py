from term.page.elements import Term


def test_close_help_screen(driver):
    page = Term(driver)
    assert page


def test_return_all_cells_from_table(driver):
    expected = 6
    page = Term(driver)
    cells = page.get_table_cells()
    assert len(cells) == expected
