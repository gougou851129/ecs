import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts.generators import ecs_helpers


class TestECSHelpers(unittest.TestCase):

    def test_is_intermediate_field(self):
        pseudo_field = {'field_details': {}}
        self.assertEqual(ecs_helpers.is_intermediate(pseudo_field), False)
        pseudo_field['field_details']['intermediate'] = False
        self.assertEqual(ecs_helpers.is_intermediate(pseudo_field), False)
        pseudo_field['field_details']['intermediate'] = True
        self.assertEqual(ecs_helpers.is_intermediate(pseudo_field), True)

    # dict_copy_existing_keys

    def test_dict_copy_existing_keys(self):
        source = {'key1': 'value1'}
        destination = {}
        ecs_helpers.dict_copy_existing_keys(source, destination, ['key1', 'missingkey'])
        self.assertEqual(destination, {'key1': 'value1'})

    def test_dict_copy_existing_keys_overwrites(self):
        source = {'key1': 'new_value'}
        destination = {'key1': 'overwritten', 'untouched': 'untouched'}
        ecs_helpers.dict_copy_existing_keys(source, destination, ['key1', 'untouched'])
        self.assertEqual(destination, {'key1': 'new_value', 'untouched': 'untouched'})

    # dict_sorted_by_keys

    def test_sorted_by_one_key(self):
        dict = {
            'message': {'name': 'message'},
            'labels': {'name': 'labels'},
            '@timestamp': {'name': '@timestamp'},
            'tags': {'name': 'tags'}
        }
        expected = [
            {'name': '@timestamp'},
            {'name': 'labels'},
            {'name': 'message'},
            {'name': 'tags'}
        ]
        result = ecs_helpers.dict_sorted_by_keys(dict, 'name')
        self.assertEqual(result, expected)
        result = ecs_helpers.dict_sorted_by_keys(dict, ['name'])
        self.assertEqual(result, expected)

    def test_sorted_by_multiple_keys(self):
        dict = {
            'cloud': {'group': 2, 'name': 'cloud'},
            'agent': {'group': 2, 'name': 'agent'},
            'base': {'group': 1, 'name': 'base'},
        }
        expected = [
            {'group': 1, 'name': 'base'},
            {'group': 2, 'name': 'agent'},
            {'group': 2, 'name': 'cloud'}
        ]
        result = ecs_helpers.dict_sorted_by_keys(dict, ['group', 'name'])
        self.assertEqual(result, expected)

    def test_merge_dicts(self):
        a = {
            'cloud': {'group': 2, 'name': 'cloud'},
            'agent': {'group': 2, 'name': 'agent'},
        }
        b = {'base': {'group': 1, 'name': 'base'}}

        result = ecs_helpers.safe_merge_dicts(a, b)

        self.assertEqual(result,
                         {
                             'cloud': {'group': 2, 'name': 'cloud'},
                             'agent': {'group': 2, 'name': 'agent'},
                             'base': {'group': 1, 'name': 'base'}
                         })

    def test_merge_dicts_raises_if_duplicate_key_added(self):
        a = {'cloud': {'group': 2, 'name': 'cloud'}}
        b = {'cloud': {'group': 9, 'name': 'bazbar'}}

        with self.assertRaises(ValueError):
            ecs_helpers.safe_merge_dicts(a, b)

    def test_clean_string_values(self):
        dict = {'dirty': ' space, the final frontier  ', 'clean': 'val', 'int': 1}
        ecs_helpers.dict_clean_string_values(dict)
        self.assertEqual(dict, {'dirty': 'space, the final frontier', 'clean': 'val', 'int': 1})

    # List helper tests

    def test_list_subtract(self):
        self.assertEqual(ecs_helpers.list_subtract(['a', 'b'], ['a']), ['b'])
        self.assertEqual(ecs_helpers.list_subtract(['a', 'b'], ['a', 'c']), ['b'])

    def test_get_tree_by_ref(self):
        ref = 'v1.5.0'
        tree = ecs_helpers.get_tree_by_ref(ref)
        self.assertEqual(tree.hexsha, '4449df245f6930d59bcd537a5958891261a9476b')


if __name__ == '__main__':
    unittest.main()
