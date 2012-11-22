import unittest

import olap.xmla.utils as utils

class TestUtils(unittest.TestCase):

    def testaslist(self):
        for x in ["Blah", None, {}, 7, (), set([1,2,3]), True]:
            self.assertIsInstance( utils.aslist(x), list)

        x = ["blah"]
        self.assertEqual( utils.aslist(x), x)

    def testschemaNameToMethodName(self):
        mn=utils.schemaNameToMethodName
        self.assertEqual(mn("DBSCHEMA_palim"), "getDBSchemaPalim")
        self.assertEqual(mn("MDSCHEMA_palim"), "getMDSchemaPalim")
        self.assertEqual(mn("DISCOVER_palim"), "getPalim")
        self.assertEqual(mn("I_KNOW_WHAT_YOU_DID_LAST_SPRINGBREAK"), 
                         "getIKnowWhatYouDidLastSpringbreak")

if __name__ == "__main__":
    unittest.main()
