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

    def testETAA(self):
        import lxml.etree as etree
        root = etree.Element("root")
        c1 = etree.SubElement(root, "c1")
        c1.text="iam_c1"
        c11 = etree.SubElement(c1, "c11")
        c11.text="iam_c11"
        c12 = etree.SubElement(c1, "c12", attrib={"a1":"val_a1", "a2":"val_a2"})
        c12.text="iam_c12"
        c2 = etree.SubElement(root, "c2")
        c2.text="iam_c2"
        etaa = utils.ETAttrAccess(root)
        self.assertEqual(etaa.c1.text, "iam_c1")
        self.assertEqual(etaa.c1.c12.text, "iam_c12")
        self.assertEqual(etaa.c1.c12._a1, "val_a1")

    def testFromETree(self):
        import lxml.etree as etree
        root = etree.Element("root")
        c1 = etree.SubElement(root, "c1")
        c1.text="iam_c1"
        c11 = etree.SubElement(c1, "c11")
        c11.text="iam_c11"
        c12 = etree.SubElement(c1, "c12", attrib={"a1":"val_a1", "a2":"val_a2"})
        c12.text="iam_c12"
        c2 = etree.SubElement(root, "c2")
        c2.text="iam_c2"
        d = utils.fromETree(root, ns="")
        self.assertEqual(d.c1.text, "iam_c1")
        self.assertEqual(d.c1.c12.text, "iam_c12")
        self.assertEqual(d.c1.c12._a1, "val_a1")

if __name__ == "__main__":
    unittest.main()
