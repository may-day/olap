# -*- coding: utf-8
"""
select {([Measures].[Customer Count]), ([Measures].[Sales Count])} 
               * {([Time].[1997].[Q2].[4]), ([Time].[1997].[Q2].[5]) } on columns, 
        [Gender].[Gender].ALLMEMBERS on rows 
        from [Sales]

"""

result={'Axes': {'Axis': [{'Tuples': {'Tuple': [{'Member': [{'Caption': 'Customer '
                                                                 'Count',
                                                      'DisplayInfo': '0',
                                                      'LName': '[Measures].[MeasuresLevel]',
                                                      'LNum': '0',
                                                      'UName': '[Measures].[Customer '
                                                               'Count]',
                                                      '_Hierarchy': 'Measures',
                                                      'text': None},
                                                     {'Caption': '4',
                                                      'DisplayInfo': '0',
                                                      'LName': '[Time].[Month]',
                                                      'LNum': '2',
                                                      'UName': '[Time].[1997].[Q2].[4]',
                                                      '_Hierarchy': 'Time',
                                                      'text': None}],
                                          'text': None},
                                         {'Member': [{'Caption': 'Customer '
                                                                 'Count',
                                                      'DisplayInfo': '0',
                                                      'LName': '[Measures].[MeasuresLevel]',
                                                      'LNum': '0',
                                                      'UName': '[Measures].[Customer '
                                                               'Count]',
                                                      '_Hierarchy': 'Measures',
                                                      'text': None},
                                                     {'Caption': '5',
                                                      'DisplayInfo': '131072',
                                                      'LName': '[Time].[Month]',
                                                      'LNum': '2',
                                                      'UName': '[Time].[1997].[Q2].[5]',
                                                      '_Hierarchy': 'Time',
                                                      'text': None}],
                                          'text': None},
                                         {'Member': [{'Caption': 'Sales Count',
                                                      'DisplayInfo': '0',
                                                      'LName': '[Measures].[MeasuresLevel]',
                                                      'LNum': '0',
                                                      'UName': '[Measures].[Sales '
                                                               'Count]',
                                                      '_Hierarchy': 'Measures',
                                                      'text': None},
                                                     {'Caption': '4',
                                                      'DisplayInfo': '131072',
                                                      'LName': '[Time].[Month]',
                                                      'LNum': '2',
                                                      'UName': '[Time].[1997].[Q2].[4]',
                                                      '_Hierarchy': 'Time',
                                                      'text': None}],
                                          'text': None},
                                         {'Member': [{'Caption': 'Sales Count',
                                                      'DisplayInfo': '0',
                                                      'LName': '[Measures].[MeasuresLevel]',
                                                      'LNum': '0',
                                                      'UName': '[Measures].[Sales '
                                                               'Count]',
                                                      '_Hierarchy': 'Measures',
                                                      'text': None},
                                                     {'Caption': '5',
                                                      'DisplayInfo': '131072',
                                                      'LName': '[Time].[Month]',
                                                      'LNum': '2',
                                                      'UName': '[Time].[1997].[Q2].[5]',
                                                      '_Hierarchy': 'Time',
                                                      'text': None}],
                                          'text': None}],
                               'text': None},
                    '_name': 'Axis0',
                    'text': None},
                   {'Tuples': {'Tuple': [{'Member': {'Caption': 'F',
                                                     'DisplayInfo': '0',
                                                     'LName': '[Gender].[Gender]',
                                                     'LNum': '1',
                                                     'UName': '[Gender].[F]',
                                                     '_Hierarchy': 'Gender',
                                                     'text': None},
                                          'text': None},
                                         {'Member': {'Caption': 'M',
                                                     'DisplayInfo': '131072',
                                                     'LName': '[Gender].[Gender]',
                                                     'LNum': '1',
                                                     'UName': '[Gender].[M]',
                                                     '_Hierarchy': 'Gender',
                                                     'text': None},
                                          'text': None}],
                               'text': None},
                    '_name': 'Axis1',
                    'text': None},
                   {'Tuples': {'Tuple': None, 'text': None},
                    '_name': 'SlicerAxis',
                    'text': None}],
          'text': None},
 'CellData': {'Cell': [{'FmtValue': '657',
                        'FormatString': '#,###',
                        'Value': 657,
                        '_CellOrdinal': '0',
                        'text': None},
                       {'FmtValue': '672',
                        'FormatString': '#,###',
                        'Value': 672,
                        '_CellOrdinal': '1',
                        'text': None},
                       {'FmtValue': '3.251',
                        'FormatString': '#,###',
                        'Value': 3251,
                        '_CellOrdinal': '2',
                        'text': None},
                       {'FmtValue': '3.438',
                        'FormatString': '#,###',
                        'Value': 3438,
                        '_CellOrdinal': '3',
                        'text': None},
                       {'FmtValue': '660',
                        'FormatString': '#,###',
                        'Value': 660,
                        '_CellOrdinal': '4',
                        'text': None},
                       {'FmtValue': '699',
                        'FormatString': '#,###',
                        'Value': 699,
                        '_CellOrdinal': '5',
                        'text': None},
                       {'FmtValue': '3.339',
                        'FormatString': '#,###',
                        'Value': 3339,
                        '_CellOrdinal': '6',
                        'text': None},
                       {'FmtValue': '3.428',
                        'FormatString': '#,###',
                        'Value': 3428,
                        '_CellOrdinal': '7',
                        'text': None}],
              'text': None},
 'OlapInfo': {'AxesInfo': {'AxisInfo': [{'HierarchyInfo': [{'Caption': {'_name': '[Measures].[MEMBER_CAPTION]',
                                                                        'text': None},
                                                            'DisplayInfo': {'_name': '[Measures].[DISPLAY_INFO]',
                                                                            'text': None},
                                                            'LName': {'_name': '[Measures].[LEVEL_UNIQUE_NAME]',
                                                                      'text': None},
                                                            'LNum': {'_name': '[Measures].[LEVEL_NUMBER]',
                                                                     'text': None},
                                                            'UName': {'_name': '[Measures].[MEMBER_UNIQUE_NAME]',
                                                                      'text': None},
                                                            '_name': 'Measures',
                                                            'text': None},
                                                           {'Caption': {'_name': '[Time].[MEMBER_CAPTION]',
                                                                        'text': None},
                                                            'DisplayInfo': {'_name': '[Time].[DISPLAY_INFO]',
                                                                            'text': None},
                                                            'LName': {'_name': '[Time].[LEVEL_UNIQUE_NAME]',
                                                                      'text': None},
                                                            'LNum': {'_name': '[Time].[LEVEL_NUMBER]',
                                                                     'text': None},
                                                            'UName': {'_name': '[Time].[MEMBER_UNIQUE_NAME]',
                                                                      'text': None},
                                                            '_name': 'Time',
                                                            'text': None}],
                                         '_name': 'Axis0',
                                         'text': None},
                                        {'HierarchyInfo': {'Caption': {'_name': '[Gender].[MEMBER_CAPTION]',
                                                                       'text': None},
                                                           'DisplayInfo': {'_name': '[Gender].[DISPLAY_INFO]',
                                                                           'text': None},
                                                           'LName': {'_name': '[Gender].[LEVEL_UNIQUE_NAME]',
                                                                     'text': None},
                                                           'LNum': {'_name': '[Gender].[LEVEL_NUMBER]',
                                                                    'text': None},
                                                           'UName': {'_name': '[Gender].[MEMBER_UNIQUE_NAME]',
                                                                     'text': None},
                                                           '_name': 'Gender',
                                                           'text': None},
                                         '_name': 'Axis1',
                                         'text': None},
                                        {'_name': 'SlicerAxis', 'text': None}],
                           'text': None},
              'CellInfo': {'FmtValue': {'_name': 'FORMATTED_VALUE',
                                        'text': None},
                           'FormatString': {'_name': 'FORMAT_STRING',
                                            'text': None},
                           'Value': {'_name': 'VALUE', 'text': None},
                           'text': None},
              'CubeInfo': {'Cube': {'CubeName': 'Sales', 'text': None},
                           'text': None},
              'text': None},
 'text': None}

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
            <HierarchyInfo name="Measures">
              <UName name="[Measures].[MEMBER_UNIQUE_NAME]"/>
              <Caption name="[Measures].[MEMBER_CAPTION]"/>
              <LName name="[Measures].[LEVEL_UNIQUE_NAME]"/>
              <LNum name="[Measures].[LEVEL_NUMBER]"/>
              <DisplayInfo name="[Measures].[DISPLAY_INFO]"/>
            </HierarchyInfo>
            <HierarchyInfo name="Time">
              <UName name="[Time].[MEMBER_UNIQUE_NAME]"/>
              <Caption name="[Time].[MEMBER_CAPTION]"/>
              <LName name="[Time].[LEVEL_UNIQUE_NAME]"/>
              <LNum name="[Time].[LEVEL_NUMBER]"/>
              <DisplayInfo name="[Time].[DISPLAY_INFO]"/>
            </HierarchyInfo>
          </AxisInfo>
          <AxisInfo name="Axis1">
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
              <Member Hierarchy="Measures">
                <UName>[Measures].[Customer Count]</UName>
                <Caption>Customer Count</Caption>
                <LName>[Measures].[MeasuresLevel]</LName>
                <LNum>0</LNum>
                <DisplayInfo>0</DisplayInfo>
              </Member>
              <Member Hierarchy="Time">
                <UName>[Time].[1997].[Q2].[4]</UName>
                <Caption>4</Caption>
                <LName>[Time].[Month]</LName>
                <LNum>2</LNum>
                <DisplayInfo>0</DisplayInfo>
              </Member>
            </Tuple>
            <Tuple>
              <Member Hierarchy="Measures">
                <UName>[Measures].[Customer Count]</UName>
                <Caption>Customer Count</Caption>
                <LName>[Measures].[MeasuresLevel]</LName>
                <LNum>0</LNum>
                <DisplayInfo>0</DisplayInfo>
              </Member>
              <Member Hierarchy="Time">
                <UName>[Time].[1997].[Q2].[5]</UName>
                <Caption>5</Caption>
                <LName>[Time].[Month]</LName>
                <LNum>2</LNum>
                <DisplayInfo>131072</DisplayInfo>
              </Member>
            </Tuple>
            <Tuple>
              <Member Hierarchy="Measures">
                <UName>[Measures].[Sales Count]</UName>
                <Caption>Sales Count</Caption>
                <LName>[Measures].[MeasuresLevel]</LName>
                <LNum>0</LNum>
                <DisplayInfo>0</DisplayInfo>
              </Member>
              <Member Hierarchy="Time">
                <UName>[Time].[1997].[Q2].[4]</UName>
                <Caption>4</Caption>
                <LName>[Time].[Month]</LName>
                <LNum>2</LNum>
                <DisplayInfo>131072</DisplayInfo>
              </Member>
            </Tuple>
            <Tuple>
              <Member Hierarchy="Measures">
                <UName>[Measures].[Sales Count]</UName>
                <Caption>Sales Count</Caption>
                <LName>[Measures].[MeasuresLevel]</LName>
                <LNum>0</LNum>
                <DisplayInfo>0</DisplayInfo>
              </Member>
              <Member Hierarchy="Time">
                <UName>[Time].[1997].[Q2].[5]</UName>
                <Caption>5</Caption>
                <LName>[Time].[Month]</LName>
                <LNum>2</LNum>
                <DisplayInfo>131072</DisplayInfo>
              </Member>
            </Tuple>
          </Tuples>
        </Axis>
        <Axis name="Axis1">
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
          <Value xsi:type="xsd:int">657</Value>
          <FmtValue>657</FmtValue>
          <FormatString>#,###</FormatString>
        </Cell>
        <Cell CellOrdinal="1">
          <Value xsi:type="xsd:int">672</Value>
          <FmtValue>672</FmtValue>
          <FormatString>#,###</FormatString>
        </Cell>
        <Cell CellOrdinal="2">
          <Value xsi:type="xsd:int">3251</Value>
          <FmtValue>3.251</FmtValue>
          <FormatString>#,###</FormatString>
        </Cell>
        <Cell CellOrdinal="3">
          <Value xsi:type="xsd:int">3438</Value>
          <FmtValue>3.438</FmtValue>
          <FormatString>#,###</FormatString>
        </Cell>
        <Cell CellOrdinal="4">
          <Value xsi:type="xsd:int">660</Value>
          <FmtValue>660</FmtValue>
          <FormatString>#,###</FormatString>
        </Cell>
        <Cell CellOrdinal="5">
          <Value xsi:type="xsd:int">699</Value>
          <FmtValue>699</FmtValue>
          <FormatString>#,###</FormatString>
        </Cell>
        <Cell CellOrdinal="6">
          <Value xsi:type="xsd:int">3339</Value>
          <FmtValue>3.339</FmtValue>
          <FormatString>#,###</FormatString>
        </Cell>
        <Cell CellOrdinal="7">
          <Value xsi:type="xsd:int">3428</Value>
          <FmtValue>3.428</FmtValue>
          <FormatString>#,###</FormatString>
        </Cell>
      </CellData>
    </root>
  </cxmla:return>
</cxmla:ExecuteResponse>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""