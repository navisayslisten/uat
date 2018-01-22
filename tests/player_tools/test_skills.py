"""UAT test file for Adventurer's Codex player tools skills module."""
import time

from selenium.webdriver.support import expected_conditions as EC # noqa

from components.character import features
from components.character.tabs import Tabs
from utils import utils as ut


def test_add_feature(player_wizard, browser): # noqa
    """As a player, I can add a feature."""
    print('As a player, I can add a feature.')

    feature = features.FeatureAddModal(browser)
    features_table = features.FeaturesTable(browser)
    tabs = Tabs(browser)
    tabs.skills.click()

    features_table.add.click()
    feature.name = 'Add Name'
    feature.class_ = 'Add Class'
    feature.level = 1
    feature.description = 'Add Description'
    feature.tracked.click()
    feature.max_.clear()
    feature.max_ = 4
    feature.short_rest.click()

    assert feature.name.get_attribute('value') == 'Add Name'
    assert feature.class_.get_attribute('value') == 'Add Class'
    assert feature.level.get_attribute('value') == '1'
    assert feature.description.get_attribute('value') == 'Add Description'
    assert feature.max_.get_attribute('value') == '4'
    assert 'active' in feature.short_rest.get_attribute('class')

    feature.add.click()

    row = ut.get_table_row(features_table, 'table', 1)

    assert row.class_ == 'Add Class'
    assert row.feature == 'Add Name'

def test_feature_ogl_pre_pop(player_wizard, browser): # noqa
    """As a player, if I select from feature name field, OGL data auto-completes and the remaining fields pre-populate."""
    print('As a player, if I select from feature name field, OGL data auto-completes and the remaining fields pre-populate.')

    feature = features.FeatureAddModal(browser)
    features_table = features.FeaturesTable(browser)
    tabs = Tabs(browser)
    tabs.skills.click()

    features_table.add.click()
    ut.select_from_autocomplete(feature, 'name', '', browser)
    feature.add.click()

    row = ut.get_table_row(features_table, 'table', 1)

    assert row.class_ == 'Barbarian'
    assert row.feature == 'Rage'

def test_delete_feature(player_wizard, browser): # noqa
    """As a player, I can delete a feature."""
    print('As a player, I can delete a feature.')

    feature = features.FeatureAddModal(browser)
    features_table = features.FeaturesTable(browser)
    tabs = Tabs(browser)
    tabs.skills.click()

    features_table.add.click()
    ut.select_from_autocomplete(feature, 'name', '', browser)
    feature.add.click()

    rows = ut.get_table_rows(features_table, 'table', values=False)
    time.sleep(.3)
    rows[0][2].click()
    rows = ut.get_table_rows(features_table, 'table', values=False)

    assert rows[0][0].text == 'Add a new Feature'

def test_add_feature(player_wizard, browser): # noqa
    """As a player, if I start typing in the name field and class field, I can select suggested items in the dropdown."""
    print('As a player, if I start typing in the name field and class field, I can select suggested items in the dropdown.')

    feature = features.FeatureAddModal(browser)
    features_table = features.FeaturesTable(browser)
    tabs = Tabs(browser)
    tabs.skills.click()

    features_table.add.click()
    ut.select_from_autocomplete(feature, 'name', '', browser)
    ut.select_from_autocomplete(feature, 'class_', '', browser)

    assert feature.name.get_attribute('value') == 'Rage (Barbarian, Lvl. 1)'
    assert feature.class_.get_attribute('value') == 'Barbarian'


def test_add_feature_open_model_by_row(player_wizard, browser): # noqa
    """As a player, I can click the first row in feature table to open the feature add modal."""
    print('As a player, I can click the first row in feature table to open the feature add modal.')

    features_table = features.FeaturesTable(browser)
    tabs = Tabs(browser)
    tabs.skills.click()

    rows = ut.get_table_rows(features_table, 'table', values=False)

    assert rows[0][0].is_enabled()
    assert rows[0][0].is_displayed()


def test_edit_feature(player_wizard, browser): # noqa
    """As a player, I can edit a feature."""
    print('As a player, I can edit a feature.')

    feature = features.FeatureAddModal(browser)
    feature_edit = features.FeatureEditModal(browser)
    features_table = features.FeaturesTable(browser)
    feature_tabs = features.FeatureModalTabs(browser)
    tabs = Tabs(browser)
    tabs.skills.click()

    features_table.add.click()
    ut.select_from_autocomplete(feature, 'name', '', browser)
    feature.add.click()

    rows = ut.get_table_rows(features_table, 'table', values=False)
    time.sleep(.3)
    rows[0][0].click()
    time.sleep(.3)
    feature_tabs.edit.click()

    feature_edit.name.clear()
    feature_edit.class_.clear()
    feature_edit.level.clear()
    feature_edit.description.clear()

    feature_edit.name = 'Edited Name'
    feature_edit.class_ = 'Edited Class'
    feature_edit.level = 1
    feature_edit.description = 'Edited Description'
    feature_edit.tracked.click()
    feature_edit.max_.clear()
    feature_edit.max_ = 4
    feature_edit.short_rest.click()

    assert feature_edit.name.get_attribute('value') == 'Edited Name'
    assert feature_edit.class_.get_attribute('value') == 'Edited Class'
    assert feature_edit.level.get_attribute('value') == '1'
    assert feature_edit.description.get_attribute('value') == 'Edited Description'
    assert feature_edit.max_.get_attribute('value') == '4'
    assert 'active' in feature_edit.short_rest.get_attribute('class')
    feature_edit.done.click()

    rows = ut.get_table_rows(features_table, 'table', values=False)
    time.sleep(.3)

    row = ut.get_table_row(features_table, 'table', 1)
    assert row.feature == 'Edited Name'
    assert row.class_ == 'Edited Class'
