import unittest

import olap.xmla.utils as utils

class TestUtils(unittest.TestCase):

    def testaslist(self):
        for x in ["Blah", None, {}, 7, (), set([1,2,3]), True]:
            self.assertIsInstance( utils.aslist(x), list)

        x = ["blah"]
        self.assertEqual( utils.aslist(x), x)

    def testListify(self):

        self.assertEqual( utils.listify(None), [None])
        self.assertEqual( utils.listify([]), [])
        # simple
        x = [[("prop", "value")]]
        self.assertEqual( utils.listify(x), [{"prop":"value"}])
        # fuse
        x = [[("prop", "value"), ("prop2", 3)]]
        self.assertEqual( utils.listify(x), [{"prop":"value", "prop2":3}])
        # recursive
        y = [[("prop", x), ("prop2", 3)]]
        self.assertEqual( utils.listify(y), [{'prop': [{'prop': 'value', 'prop2': 3}], 
                                              'prop2': 3}])
        # multiple records
        x = [[("prop", "value"), ("prop2", 3)], [("prop3", "value"), ("prop4", 3)]]
        self.assertEqual( utils.listify(x), [{'prop': 'value', 'prop2': 3}, 
                                             {'prop3': 'value', 'prop4': 3}])

    def testMapify(self):
        # key the records based on a property
        x = [[("prop", "value1"), ("prop2", 3)], [("prop", "value2"), ("prop2", 44)]]
        self.assertEqual( utils.mapify(x, "prop"), {'value1': {'prop': 'value1', 'prop2': 3},
                                                    'value2': {'prop': 'value2', 'prop2': 44}
                                                    })

    def testschemaNameToMethodName(self):
        mn=utils.schemaNameToMethodName
        self.assertEqual(mn("DBSCHEMA_palim"), "getDBSchemaPalim")
        self.assertEqual(mn("MDSCHEMA_palim"), "getMDSchemaPalim")
        self.assertEqual(mn("DISCOVER_palim"), "getPalim")
        self.assertEqual(mn("I_KNOW_WHAT_YOU_DID_LAST_SPRINGBREAK"), 
                         "getIKnowWhatYouDidLastSpringbreak")

if __name__ == "__main__":
    unittest.main()
