# -*- coding: utf-8
"""
select [Gender].[Gender].ALLMEMBERS on columns from [Sales]

"""

result={'Axes': {'Axis': [{'Tuples': {'Tuple': [{'Member': {'Caption': 'F',
                                                     'DisplayInfo': '0',
                                                     'LName': '[Gender].[Gender]',
                                                     'LNum': '1',
                                                     'UName': '[Gender].[F]',
                                                     '_Hierarchy': 'Gender'}},
                                         {'Member': {'Caption': 'M',
                                                     'DisplayInfo': '131072',
                                                     'LName': '[Gender].[Gender]',
                                                     'LNum': '1',
                                                     'UName': '[Gender].[M]',
                                                     '_Hierarchy': 'Gender'}}]},
                    '_name': 'Axis0'},
                   {'Tuples': {'Tuple': None}, '_name': 'SlicerAxis'}]},
 'CellData': {'Cell': [{'FmtValue': '131.558',
                        'FormatString': 'Standard',
                        'Value': 131558.0,
                        '_CellOrdinal': '0'},
                       {'FmtValue': '135.215',
                        'FormatString': 'Standard',
                        'Value': 135215.0,
                        '_CellOrdinal': '1'}]},
 'OlapInfo': {'AxesInfo': {'AxisInfo': [{'HierarchyInfo': {'Caption': {'_name': '[Gender].[MEMBER_CAPTION]'},
                                                           'DisplayInfo': {'_name': '[Gender].[DISPLAY_INFO]'},
                                                           'LName': {'_name': '[Gender].[LEVEL_UNIQUE_NAME]'},
                                                           'LNum': {'_name': '[Gender].[LEVEL_NUMBER]'},
                                                           'UName': {'_name': '[Gender].[MEMBER_UNIQUE_NAME]'},
                                                           '_name': 'Gender'},
                                         '_name': 'Axis0'},
                                        {'_name': 'SlicerAxis'}]},
              'CellInfo': {'FmtValue': {'_name': 'FORMATTED_VALUE'},
                           'FormatString': {'_name': 'FORMAT_STRING'},
                           'Value': {'_name': 'VALUE'}},
              'CubeInfo': {'Cube': {'CubeName': 'Sales'}}}}

xml_response="""<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
<SOAP-ENV:Header>
</SOAP-ENV:Header>
<SOAP-ENV:Body>
<cxmla:ExecuteResponse xmlns:cxmla="urn:schemas-microsoft-com:xml-analysis">
  <cxmla:return>
    <root xmlns="urn:schemas-microsoft-com:xml-analysis:mddataset" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:EX="urn:schemas-microsoft-com:xml-analysis:exception">
      <xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="urn:schemas-microsoft-com:xml-analysis:mddataset" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:sql="urn:schemas-microsoft-com:xml-sql" targetNamespace="urn:schemas-microsoft-com:xml-analysis:mddataset" elementFormDefault="qualified">
        <xsd:complexType name="MemberType">
          <xsd:sequence>
            <xsd:element name="UName" type="xsd:string"/>
            <xsd:element name="Caption" type="xsd:string"/>
            <xsd:element name="LName" type="xsd:string"/>
            <xsd:element name="LNum" type="xsd:unsignedInt"/>
            <xsd:element name="DisplayInfo" type="xsd:unsignedInt"/>
            <xsd:sequence maxOccurs="unbounded" minOccurs="0">
              <xsd:any processContents="lax" maxOccurs="unbounded"/>
            </xsd:sequence>
          </xsd:sequence>
          <xsd:attribute name="Hierarchy" type="xsd:string"/>
        </xsd:complexType>
        <xsd:complexType name="PropType">
          <xsd:attribute name="name" type="xsd:string"/>
        </xsd:complexType>
        <xsd:complexType name="TupleType">
          <xsd:sequence maxOccurs="unbounded">
            <xsd:element name="Member" type="MemberType"/>
          </xsd:sequence>
        </xsd:complexType>
        <xsd:complexType name="MembersType">
          <xsd:sequence maxOccurs="unbounded">
            <xsd:element name="Member" type="MemberType"/>
          </xsd:sequence>
          <xsd:attribute name="Hierarchy" type="xsd:string"/>
        </xsd:complexType>
        <xsd:complexType name="TuplesType">
          <xsd:sequence maxOccurs="unbounded">
            <xsd:element name="Tuple" type="TupleType"/>
          </xsd:sequence>
        </xsd:complexType>
        <xsd:complexType name="CrossProductType">
          <xsd:sequence>
            <xsd:choice minOccurs="0" maxOccurs="unbounded">
              <xsd:element name="Members" type="MembersType"/>
              <xsd:element name="Tuples" type="TuplesType"/>
            </xsd:choice>
          </xsd:sequence>
          <xsd:attribute name="Size" type="xsd:unsignedInt"/>
        </xsd:complexType>
        <xsd:complexType name="OlapInfo">
          <xsd:sequence>
            <xsd:element name="CubeInfo">
              <xsd:complexType>
                <xsd:sequence>
                  <xsd:element name="Cube" maxOccurs="unbounded">
                    <xsd:complexType>
                      <xsd:sequence>
                        <xsd:element name="CubeName" type="xsd:string"/>
                      </xsd:sequence>
                    </xsd:complexType>
                  </xsd:element>
                </xsd:sequence>
              </xsd:complexType>
            </xsd:element>
            <xsd:element name="AxesInfo">
              <xsd:complexType>
                <xsd:sequence>
                  <xsd:element name="AxisInfo" maxOccurs="unbounded">
                    <xsd:complexType>
                      <xsd:sequence>
                        <xsd:element name="HierarchyInfo" minOccurs="0" maxOccurs="unbounded">
                          <xsd:complexType>
                            <xsd:sequence>
                              <xsd:sequence maxOccurs="unbounded">
                                <xsd:element name="UName" type="PropType"/>
                                <xsd:element name="Caption" type="PropType"/>
                                <xsd:element name="LName" type="PropType"/>
                                <xsd:element name="LNum" type="PropType"/>
                                <xsd:element name="DisplayInfo" type="PropType" minOccurs="0" maxOccurs="unbounded"/>
                              </xsd:sequence>
                              <xsd:sequence>
                                <xsd:any processContents="lax" minOccurs="0" maxOccurs="unbounded"/>
                              </xsd:sequence>
                            </xsd:sequence>
                            <xsd:attribute name="name" type="xsd:string" use="required"/>
                          </xsd:complexType>
                        </xsd:element>
                      </xsd:sequence>
                      <xsd:attribute name="name" type="xsd:string"/>
                    </xsd:complexType>
                  </xsd:element>
                </xsd:sequence>
              </xsd:complexType>
            </xsd:element>
            <xsd:element name="CellInfo">
              <xsd:complexType>
                <xsd:sequence>
                  <xsd:sequence minOccurs="0" maxOccurs="unbounded">
                    <xsd:choice>
                      <xsd:element name="Value" type="PropType"/>
                      <xsd:element name="FmtValue" type="PropType"/>
                      <xsd:element name="BackColor" type="PropType"/>
                      <xsd:element name="ForeColor" type="PropType"/>
                      <xsd:element name="FontName" type="PropType"/>
                      <xsd:element name="FontSize" type="PropType"/>
                      <xsd:element name="FontFlags" type="PropType"/>
                      <xsd:element name="FormatString" type="PropType"/>
                      <xsd:element name="NonEmptyBehavior" type="PropType"/>
                      <xsd:element name="SolveOrder" type="PropType"/>
                      <xsd:element name="Updateable" type="PropType"/>
                      <xsd:element name="Visible" type="PropType"/>
                      <xsd:element name="Expression" type="PropType"/>
                    </xsd:choice>
                  </xsd:sequence>
                  <xsd:sequence maxOccurs="unbounded" minOccurs="0">
                    <xsd:any processContents="lax" maxOccurs="unbounded"/>
                  </xsd:sequence>
                </xsd:sequence>
              </xsd:complexType>
            </xsd:element>
          </xsd:sequence>
        </xsd:complexType>
        <xsd:complexType name="Axes">
          <xsd:sequence maxOccurs="unbounded">
            <xsd:element name="Axis">
              <xsd:complexType>
                <xsd:choice minOccurs="0" maxOccurs="unbounded">
                  <xsd:element name="CrossProduct" type="CrossProductType"/>
                  <xsd:element name="Tuples" type="TuplesType"/>
                  <xsd:element name="Members" type="MembersType"/>
                </xsd:choice>
                <xsd:attribute name="name" type="xsd:string"/>
              </xsd:complexType>
            </xsd:element>
          </xsd:sequence>
        </xsd:complexType>
        <xsd:complexType name="CellData">
          <xsd:sequence>
            <xsd:element name="Cell" minOccurs="0" maxOccurs="unbounded">
              <xsd:complexType>
                <xsd:sequence maxOccurs="unbounded">
                  <xsd:choice>
                    <xsd:element name="Value"/>
                    <xsd:element name="FmtValue" type="xsd:string"/>
                    <xsd:element name="BackColor" type="xsd:unsignedInt"/>
                    <xsd:element name="ForeColor" type="xsd:unsignedInt"/>
                    <xsd:element name="FontName" type="xsd:string"/>
                    <xsd:element name="FontSize" type="xsd:unsignedShort"/>
                    <xsd:element name="FontFlags" type="xsd:unsignedInt"/>
                    <xsd:element name="FormatString" type="xsd:string"/>
                    <xsd:element name="NonEmptyBehavior" type="xsd:unsignedShort"/>
                    <xsd:element name="SolveOrder" type="xsd:unsignedInt"/>
                    <xsd:element name="Updateable" type="xsd:unsignedInt"/>
                    <xsd:element name="Visible" type="xsd:unsignedInt"/>
                    <xsd:element name="Expression" type="xsd:string"/>
                  </xsd:choice>
                </xsd:sequence>
                <xsd:attribute name="CellOrdinal" type="xsd:unsignedInt" use="required"/>
              </xsd:complexType>
            </xsd:element>
          </xsd:sequence>
        </xsd:complexType>
        <xsd:element name="root">
          <xsd:complexType>
            <xsd:sequence maxOccurs="unbounded">
              <xsd:element name="OlapInfo" type="OlapInfo"/>
              <xsd:element name="Axes" type="Axes"/>
              <xsd:element name="CellData" type="CellData"/>
            </xsd:sequence>
          </xsd:complexType>
        </xsd:element>
      </xsd:schema>
      <OlapInfo>
        <CubeInfo>
          <Cube>
            <CubeName>Sales</CubeName>
          </Cube>
        </CubeInfo>
        <AxesInfo>
          <AxisInfo name="Axis0">
            <HierarchyInfo name="Gender">
              <UName name="[Gender].[MEMBER_UNIQUE_NAME]"/>
              <Caption name="[Gender].[MEMBER_CAPTION]"/>
              <LName name="[Gender].[LEVEL_UNIQUE_NAME]"/>
              <LNum name="[Gender].[LEVEL_NUMBER]"/>
              <DisplayInfo name="[Gender].[DISPLAY_INFO]"/>
            </HierarchyInfo>
          </AxisInfo>
          <AxisInfo name="SlicerAxis"/>
        </AxesInfo>
        <CellInfo>
          <Value name="VALUE"/>
          <FmtValue name="FORMATTED_VALUE"/>
          <FormatString name="FORMAT_STRING"/>
        </CellInfo>
      </OlapInfo>
      <Axes>
        <Axis name="Axis0">
          <Tuples>
            <Tuple>
              <Member Hierarchy="Gender">
                <UName>[Gender].[F]</UName>
                <Caption>F</Caption>
                <LName>[Gender].[Gender]</LName>
                <LNum>1</LNum>
                <DisplayInfo>0</DisplayInfo>
              </Member>
            </Tuple>
            <Tuple>
              <Member Hierarchy="Gender">
                <UName>[Gender].[M]</UName>
                <Caption>M</Caption>
                <LName>[Gender].[Gender]</LName>
                <LNum>1</LNum>
                <DisplayInfo>131072</DisplayInfo>
              </Member>
            </Tuple>
          </Tuples>
        </Axis>
        <Axis name="SlicerAxis">
          <Tuples>
            <Tuple/>
          </Tuples>
        </Axis>
      </Axes>
      <CellData>
        <Cell CellOrdinal="0">
          <Value xsi:type="xsd:double">131558</Value>
          <FmtValue>131.558</FmtValue>
          <FormatString>Standard</FormatString>
        </Cell>
        <Cell CellOrdinal="1">
          <Value xsi:type="xsd:double">135215</Value>
          <FmtValue>135.215</FmtValue>
          <FormatString>Standard</FormatString>
        </Cell>
      </CellData>
    </root>
  </cxmla:return>
</cxmla:ExecuteResponse>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""