conversation={
    "test2Axes":[
        ("request", """<soap-env:Envelope xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/" xmlns="urn:schemas-microsoft-com:xml-analysis">
  <soap-env:Body>
    <Execute>
      <Command>
        <Statement>select {[Measures].ALLMEMBERS} * {[Time].[1997].[Q2].children} on columns, 
                       [Gender].[Gender].ALLMEMBERS on rows 
                from [Sales]</Statement>
      </Command>
      <Properties>
        <PropertyList>
          <Format>Multidimensional</Format>
          <AxisFormat>TupleFormat</AxisFormat>
          <Catalog>FoodMart</Catalog>
        </PropertyList>
      </Properties>
    </Execute>
  </soap-env:Body>
</soap-env:Envelope>
"""),
        ("response", """<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
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
                <UName>[Measures].[Unit Sales]</UName>
                <Caption>Unit Sales</Caption>
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
                <UName>[Measures].[Unit Sales]</UName>
                <Caption>Unit Sales</Caption>
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
                <UName>[Measures].[Unit Sales]</UName>
                <Caption>Unit Sales</Caption>
                <LName>[Measures].[MeasuresLevel]</LName>
                <LNum>0</LNum>
                <DisplayInfo>0</DisplayInfo>
              </Member>
              <Member Hierarchy="Time">
                <UName>[Time].[1997].[Q2].[6]</UName>
                <Caption>6</Caption>
                <LName>[Time].[Month]</LName>
                <LNum>2</LNum>
                <DisplayInfo>131072</DisplayInfo>
              </Member>
            </Tuple>
            <Tuple>
              <Member Hierarchy="Measures">
                <UName>[Measures].[Store Cost]</UName>
                <Caption>Store Cost</Caption>
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
                <UName>[Measures].[Store Cost]</UName>
                <Caption>Store Cost</Caption>
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
                <UName>[Measures].[Store Cost]</UName>
                <Caption>Store Cost</Caption>
                <LName>[Measures].[MeasuresLevel]</LName>
                <LNum>0</LNum>
                <DisplayInfo>0</DisplayInfo>
              </Member>
              <Member Hierarchy="Time">
                <UName>[Time].[1997].[Q2].[6]</UName>
                <Caption>6</Caption>
                <LName>[Time].[Month]</LName>
                <LNum>2</LNum>
                <DisplayInfo>131072</DisplayInfo>
              </Member>
            </Tuple>
            <Tuple>
              <Member Hierarchy="Measures">
                <UName>[Measures].[Store Sales]</UName>
                <Caption>Store Sales</Caption>
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
                <UName>[Measures].[Store Sales]</UName>
                <Caption>Store Sales</Caption>
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
                <UName>[Measures].[Store Sales]</UName>
                <Caption>Store Sales</Caption>
                <LName>[Measures].[MeasuresLevel]</LName>
                <LNum>0</LNum>
                <DisplayInfo>0</DisplayInfo>
              </Member>
              <Member Hierarchy="Time">
                <UName>[Time].[1997].[Q2].[6]</UName>
                <Caption>6</Caption>
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
            <Tuple>
              <Member Hierarchy="Measures">
                <UName>[Measures].[Sales Count]</UName>
                <Caption>Sales Count</Caption>
                <LName>[Measures].[MeasuresLevel]</LName>
                <LNum>0</LNum>
                <DisplayInfo>0</DisplayInfo>
              </Member>
              <Member Hierarchy="Time">
                <UName>[Time].[1997].[Q2].[6]</UName>
                <Caption>6</Caption>
                <LName>[Time].[Month]</LName>
                <LNum>2</LNum>
                <DisplayInfo>131072</DisplayInfo>
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
                <UName>[Time].[1997].[Q2].[4]</UName>
                <Caption>4</Caption>
                <LName>[Time].[Month]</LName>
                <LNum>2</LNum>
                <DisplayInfo>131072</DisplayInfo>
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
                <UName>[Measures].[Customer Count]</UName>
                <Caption>Customer Count</Caption>
                <LName>[Measures].[MeasuresLevel]</LName>
                <LNum>0</LNum>
                <DisplayInfo>0</DisplayInfo>
              </Member>
              <Member Hierarchy="Time">
                <UName>[Time].[1997].[Q2].[6]</UName>
                <Caption>6</Caption>
                <LName>[Time].[Month]</LName>
                <LNum>2</LNum>
                <DisplayInfo>131072</DisplayInfo>
              </Member>
            </Tuple>
            <Tuple>
              <Member Hierarchy="Measures">
                <UName>[Measures].[Promotion Sales]</UName>
                <Caption>Promotion Sales</Caption>
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
                <UName>[Measures].[Promotion Sales]</UName>
                <Caption>Promotion Sales</Caption>
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
                <UName>[Measures].[Promotion Sales]</UName>
                <Caption>Promotion Sales</Caption>
                <LName>[Measures].[MeasuresLevel]</LName>
                <LNum>0</LNum>
                <DisplayInfo>0</DisplayInfo>
              </Member>
              <Member Hierarchy="Time">
                <UName>[Time].[1997].[Q2].[6]</UName>
                <Caption>6</Caption>
                <LName>[Time].[Month]</LName>
                <LNum>2</LNum>
                <DisplayInfo>131072</DisplayInfo>
              </Member>
            </Tuple>
            <Tuple>
              <Member Hierarchy="Measures">
                <UName>[Measures].[Profit]</UName>
                <Caption>Profit</Caption>
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
                <UName>[Measures].[Profit]</UName>
                <Caption>Profit</Caption>
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
                <UName>[Measures].[Profit]</UName>
                <Caption>Profit</Caption>
                <LName>[Measures].[MeasuresLevel]</LName>
                <LNum>0</LNum>
                <DisplayInfo>0</DisplayInfo>
              </Member>
              <Member Hierarchy="Time">
                <UName>[Time].[1997].[Q2].[6]</UName>
                <Caption>6</Caption>
                <LName>[Time].[Month]</LName>
                <LNum>2</LNum>
                <DisplayInfo>131072</DisplayInfo>
              </Member>
            </Tuple>
            <Tuple>
              <Member Hierarchy="Measures">
                <UName>[Measures].[Profit Growth]</UName>
                <Caption>Gewinn-Wachstum</Caption>
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
                <UName>[Measures].[Profit Growth]</UName>
                <Caption>Gewinn-Wachstum</Caption>
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
                <UName>[Measures].[Profit Growth]</UName>
                <Caption>Gewinn-Wachstum</Caption>
                <LName>[Measures].[MeasuresLevel]</LName>
                <LNum>0</LNum>
                <DisplayInfo>0</DisplayInfo>
              </Member>
              <Member Hierarchy="Time">
                <UName>[Time].[1997].[Q2].[6]</UName>
                <Caption>6</Caption>
                <LName>[Time].[Month]</LName>
                <LNum>2</LNum>
                <DisplayInfo>131072</DisplayInfo>
              </Member>
            </Tuple>
            <Tuple>
              <Member Hierarchy="Measures">
                <UName>[Measures].[Profit last Period]</UName>
                <Caption>Profit last Period</Caption>
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
                <UName>[Measures].[Profit last Period]</UName>
                <Caption>Profit last Period</Caption>
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
                <UName>[Measures].[Profit last Period]</UName>
                <Caption>Profit last Period</Caption>
                <LName>[Measures].[MeasuresLevel]</LName>
                <LNum>0</LNum>
                <DisplayInfo>0</DisplayInfo>
              </Member>
              <Member Hierarchy="Time">
                <UName>[Time].[1997].[Q2].[6]</UName>
                <Caption>6</Caption>
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
          <Value xsi:type="xsd:double">9990</Value>
          <FmtValue>9.990</FmtValue>
          <FormatString>Standard</FormatString>
        </Cell>
        <Cell CellOrdinal="1">
          <Value xsi:type="xsd:double">10536</Value>
          <FmtValue>10.536</FmtValue>
          <FormatString>Standard</FormatString>
        </Cell>
        <Cell CellOrdinal="2">
          <Value xsi:type="xsd:double">10466</Value>
          <FmtValue>10.466</FmtValue>
          <FormatString>Standard</FormatString>
        </Cell>
        <Cell CellOrdinal="3">
          <Value xsi:type="xsd:double">8468.863</Value>
          <FmtValue>8.468,86</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="4">
          <Value xsi:type="xsd:double">8862.9146</Value>
          <FmtValue>8.862,91</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="5">
          <Value xsi:type="xsd:double">8977.7991</Value>
          <FmtValue>8.977,80</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="6">
          <Value xsi:type="xsd:double">21210.05</Value>
          <FmtValue>21.210,05</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="7">
          <Value xsi:type="xsd:double">22200.18</Value>
          <FmtValue>22.200,18</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="8">
          <Value xsi:type="xsd:double">22446.91</Value>
          <FmtValue>22.446,91</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="9">
          <Value xsi:type="xsd:int">3251</Value>
          <FmtValue>3.251</FmtValue>
          <FormatString>#,###</FormatString>
        </Cell>
        <Cell CellOrdinal="10">
          <Value xsi:type="xsd:int">3438</Value>
          <FmtValue>3.438</FmtValue>
          <FormatString>#,###</FormatString>
        </Cell>
        <Cell CellOrdinal="11">
          <Value xsi:type="xsd:int">3388</Value>
          <FmtValue>3.388</FmtValue>
          <FormatString>#,###</FormatString>
        </Cell>
        <Cell CellOrdinal="12">
          <Value xsi:type="xsd:int">657</Value>
          <FmtValue>657</FmtValue>
          <FormatString>#,###</FormatString>
        </Cell>
        <Cell CellOrdinal="13">
          <Value xsi:type="xsd:int">672</Value>
          <FmtValue>672</FmtValue>
          <FormatString>#,###</FormatString>
        </Cell>
        <Cell CellOrdinal="14">
          <Value xsi:type="xsd:int">650</Value>
          <FmtValue>650</FmtValue>
          <FormatString>#,###</FormatString>
        </Cell>
        <Cell CellOrdinal="15">
          <Value xsi:type="xsd:double">6108.38</Value>
          <FmtValue>6.108,38</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="16">
          <Value xsi:type="xsd:double">4695.4</Value>
          <FmtValue>4.695,40</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="17">
          <Value xsi:type="xsd:double">6606.76</Value>
          <FmtValue>6.606,76</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="18">
          <Value xsi:type="xsd:double">12741.187</Value>
          <FmtValue>$12.741,19</FmtValue>
          <FormatString>$#,##0.00</FormatString>
        </Cell>
        <Cell CellOrdinal="19">
          <Value xsi:type="xsd:double">13337.2654</Value>
          <FmtValue>$13.337,27</FmtValue>
          <FormatString>$#,##0.00</FormatString>
        </Cell>
        <Cell CellOrdinal="20">
          <Value xsi:type="xsd:double">13469.1109</Value>
          <FmtValue>$13.469,11</FmtValue>
          <FormatString>$#,##0.00</FormatString>
        </Cell>
        <Cell CellOrdinal="21">
          <Value xsi:type="xsd:double">-0.14289748385006706</Value>
          <FmtValue>-14,3%</FmtValue>
          <FormatString>0.0%</FormatString>
        </Cell>
        <Cell CellOrdinal="22">
          <Value xsi:type="xsd:double">0.04678358460636362</Value>
          <FmtValue>4,7%</FmtValue>
          <FormatString>0.0%</FormatString>
        </Cell>
        <Cell CellOrdinal="23">
          <Value xsi:type="xsd:double">0.009885497217443048</Value>
          <FmtValue>1,0%</FmtValue>
          <FormatString>0.0%</FormatString>
        </Cell>
        <Cell CellOrdinal="24">
          <Value xsi:type="xsd:double">14865.4178</Value>
          <FmtValue>$14.865,42</FmtValue>
          <FormatString>$#,##0.00</FormatString>
        </Cell>
        <Cell CellOrdinal="25">
          <Value xsi:type="xsd:double">12741.187</Value>
          <FmtValue>$12.741,19</FmtValue>
          <FormatString>$#,##0.00</FormatString>
        </Cell>
        <Cell CellOrdinal="26">
          <Value xsi:type="xsd:double">13337.2654</Value>
          <FmtValue>$13.337,27</FmtValue>
          <FormatString>$#,##0.00</FormatString>
        </Cell>
        <Cell CellOrdinal="27">
          <Value xsi:type="xsd:double">10189</Value>
          <FmtValue>10.189</FmtValue>
          <FormatString>Standard</FormatString>
        </Cell>
        <Cell CellOrdinal="28">
          <Value xsi:type="xsd:double">10545</Value>
          <FmtValue>10.545</FmtValue>
          <FormatString>Standard</FormatString>
        </Cell>
        <Cell CellOrdinal="29">
          <Value xsi:type="xsd:double">10884</Value>
          <FmtValue>10.884</FmtValue>
          <FormatString>Standard</FormatString>
        </Cell>
        <Cell CellOrdinal="30">
          <Value xsi:type="xsd:double">8642.8363</Value>
          <FmtValue>8.642,84</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="31">
          <Value xsi:type="xsd:double">8919.6411</Value>
          <FmtValue>8.919,64</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="32">
          <Value xsi:type="xsd:double">9092.1707</Value>
          <FmtValue>9.092,17</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="33">
          <Value xsi:type="xsd:double">21668.2</Value>
          <FmtValue>21.668,20</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="34">
          <Value xsi:type="xsd:double">22256.11</Value>
          <FmtValue>22.256,11</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="35">
          <Value xsi:type="xsd:double">22884.82</Value>
          <FmtValue>22.884,82</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="36">
          <Value xsi:type="xsd:int">3339</Value>
          <FmtValue>3.339</FmtValue>
          <FormatString>#,###</FormatString>
        </Cell>
        <Cell CellOrdinal="37">
          <Value xsi:type="xsd:int">3428</Value>
          <FmtValue>3.428</FmtValue>
          <FormatString>#,###</FormatString>
        </Cell>
        <Cell CellOrdinal="38">
          <Value xsi:type="xsd:int">3524</Value>
          <FmtValue>3.524</FmtValue>
          <FormatString>#,###</FormatString>
        </Cell>
        <Cell CellOrdinal="39">
          <Value xsi:type="xsd:int">660</Value>
          <FmtValue>660</FmtValue>
          <FormatString>#,###</FormatString>
        </Cell>
        <Cell CellOrdinal="40">
          <Value xsi:type="xsd:int">699</Value>
          <FmtValue>699</FmtValue>
          <FormatString>#,###</FormatString>
        </Cell>
        <Cell CellOrdinal="41">
          <Value xsi:type="xsd:int">686</Value>
          <FmtValue>686</FmtValue>
          <FormatString>#,###</FormatString>
        </Cell>
        <Cell CellOrdinal="42">
          <Value xsi:type="xsd:double">5196</Value>
          <FmtValue>5.196,00</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="43">
          <Value xsi:type="xsd:double">4906.08</Value>
          <FmtValue>4.906,08</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="44">
          <Value xsi:type="xsd:double">6318.56</Value>
          <FmtValue>6.318,56</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="45">
          <Value xsi:type="xsd:double">13025.3637</Value>
          <FmtValue>$13.025,36</FmtValue>
          <FormatString>$#,##0.00</FormatString>
        </Cell>
        <Cell CellOrdinal="46">
          <Value xsi:type="xsd:double">13336.4689</Value>
          <FmtValue>$13.336,47</FmtValue>
          <FormatString>$#,##0.00</FormatString>
        </Cell>
        <Cell CellOrdinal="47">
          <Value xsi:type="xsd:double">13792.6493</Value>
          <FmtValue>$13.792,65</FmtValue>
          <FormatString>$#,##0.00</FormatString>
        </Cell>
        <Cell CellOrdinal="48">
          <Value xsi:type="xsd:double">-0.14252509703003943</Value>
          <FmtValue>-14,3%</FmtValue>
          <FormatString>0.0%</FormatString>
        </Cell>
        <Cell CellOrdinal="49">
          <Value xsi:type="xsd:double">0.023884569150264878</Value>
          <FmtValue>2,4%</FmtValue>
          <FormatString>0.0%</FormatString>
        </Cell>
        <Cell CellOrdinal="50">
          <Value xsi:type="xsd:double">0.03420548598137542</Value>
          <FmtValue>3,4%</FmtValue>
          <FormatString>0.0%</FormatString>
        </Cell>
        <Cell CellOrdinal="51">
          <Value xsi:type="xsd:double">15190.3731</Value>
          <FmtValue>$15.190,37</FmtValue>
          <FormatString>$#,##0.00</FormatString>
        </Cell>
        <Cell CellOrdinal="52">
          <Value xsi:type="xsd:double">13025.3637</Value>
          <FmtValue>$13.025,36</FmtValue>
          <FormatString>$#,##0.00</FormatString>
        </Cell>
        <Cell CellOrdinal="53">
          <Value xsi:type="xsd:double">13336.4689</Value>
          <FmtValue>$13.336,47</FmtValue>
          <FormatString>$#,##0.00</FormatString>
        </Cell>
      </CellData>
    </root>
  </cxmla:return>
</cxmla:ExecuteResponse>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""),
    ],
    "test3Axes":[
        ("request", """<soap-env:Envelope xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/" xmlns="urn:schemas-microsoft-com:xml-analysis">
  <soap-env:Body>
    <Execute>
      <Command>
        <Statement>select [Measures].ALLMEMBERS on columns, 
                       [Time].[1997].[Q2].children on rows, [Gender].[Gender].ALLMEMBERS on Axis(2) 
                from [Sales]</Statement>
      </Command>
      <Properties>
        <PropertyList>
          <Format>Multidimensional</Format>
          <AxisFormat>TupleFormat</AxisFormat>
          <Catalog>FoodMart</Catalog>
        </PropertyList>
      </Properties>
    </Execute>
  </soap-env:Body>
</soap-env:Envelope>
"""),
        ("response", """<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
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
          </AxisInfo>
          <AxisInfo name="Axis1">
            <HierarchyInfo name="Time">
              <UName name="[Time].[MEMBER_UNIQUE_NAME]"/>
              <Caption name="[Time].[MEMBER_CAPTION]"/>
              <LName name="[Time].[LEVEL_UNIQUE_NAME]"/>
              <LNum name="[Time].[LEVEL_NUMBER]"/>
              <DisplayInfo name="[Time].[DISPLAY_INFO]"/>
            </HierarchyInfo>
          </AxisInfo>
          <AxisInfo name="Axis2">
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
                <UName>[Measures].[Unit Sales]</UName>
                <Caption>Unit Sales</Caption>
                <LName>[Measures].[MeasuresLevel]</LName>
                <LNum>0</LNum>
                <DisplayInfo>0</DisplayInfo>
              </Member>
            </Tuple>
            <Tuple>
              <Member Hierarchy="Measures">
                <UName>[Measures].[Store Cost]</UName>
                <Caption>Store Cost</Caption>
                <LName>[Measures].[MeasuresLevel]</LName>
                <LNum>0</LNum>
                <DisplayInfo>0</DisplayInfo>
              </Member>
            </Tuple>
            <Tuple>
              <Member Hierarchy="Measures">
                <UName>[Measures].[Store Sales]</UName>
                <Caption>Store Sales</Caption>
                <LName>[Measures].[MeasuresLevel]</LName>
                <LNum>0</LNum>
                <DisplayInfo>0</DisplayInfo>
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
            </Tuple>
            <Tuple>
              <Member Hierarchy="Measures">
                <UName>[Measures].[Customer Count]</UName>
                <Caption>Customer Count</Caption>
                <LName>[Measures].[MeasuresLevel]</LName>
                <LNum>0</LNum>
                <DisplayInfo>0</DisplayInfo>
              </Member>
            </Tuple>
            <Tuple>
              <Member Hierarchy="Measures">
                <UName>[Measures].[Promotion Sales]</UName>
                <Caption>Promotion Sales</Caption>
                <LName>[Measures].[MeasuresLevel]</LName>
                <LNum>0</LNum>
                <DisplayInfo>0</DisplayInfo>
              </Member>
            </Tuple>
            <Tuple>
              <Member Hierarchy="Measures">
                <UName>[Measures].[Profit]</UName>
                <Caption>Profit</Caption>
                <LName>[Measures].[MeasuresLevel]</LName>
                <LNum>0</LNum>
                <DisplayInfo>0</DisplayInfo>
              </Member>
            </Tuple>
            <Tuple>
              <Member Hierarchy="Measures">
                <UName>[Measures].[Profit Growth]</UName>
                <Caption>Gewinn-Wachstum</Caption>
                <LName>[Measures].[MeasuresLevel]</LName>
                <LNum>0</LNum>
                <DisplayInfo>0</DisplayInfo>
              </Member>
            </Tuple>
            <Tuple>
              <Member Hierarchy="Measures">
                <UName>[Measures].[Profit last Period]</UName>
                <Caption>Profit last Period</Caption>
                <LName>[Measures].[MeasuresLevel]</LName>
                <LNum>0</LNum>
                <DisplayInfo>0</DisplayInfo>
              </Member>
            </Tuple>
          </Tuples>
        </Axis>
        <Axis name="Axis1">
          <Tuples>
            <Tuple>
              <Member Hierarchy="Time">
                <UName>[Time].[1997].[Q2].[4]</UName>
                <Caption>4</Caption>
                <LName>[Time].[Month]</LName>
                <LNum>2</LNum>
                <DisplayInfo>0</DisplayInfo>
              </Member>
            </Tuple>
            <Tuple>
              <Member Hierarchy="Time">
                <UName>[Time].[1997].[Q2].[5]</UName>
                <Caption>5</Caption>
                <LName>[Time].[Month]</LName>
                <LNum>2</LNum>
                <DisplayInfo>131072</DisplayInfo>
              </Member>
            </Tuple>
            <Tuple>
              <Member Hierarchy="Time">
                <UName>[Time].[1997].[Q2].[6]</UName>
                <Caption>6</Caption>
                <LName>[Time].[Month]</LName>
                <LNum>2</LNum>
                <DisplayInfo>131072</DisplayInfo>
              </Member>
            </Tuple>
          </Tuples>
        </Axis>
        <Axis name="Axis2">
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
          <Value xsi:type="xsd:double">9990</Value>
          <FmtValue>9.990</FmtValue>
          <FormatString>Standard</FormatString>
        </Cell>
        <Cell CellOrdinal="1">
          <Value xsi:type="xsd:double">8468.863</Value>
          <FmtValue>8.468,86</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="2">
          <Value xsi:type="xsd:double">21210.05</Value>
          <FmtValue>21.210,05</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="3">
          <Value xsi:type="xsd:int">3251</Value>
          <FmtValue>3.251</FmtValue>
          <FormatString>#,###</FormatString>
        </Cell>
        <Cell CellOrdinal="4">
          <Value xsi:type="xsd:int">657</Value>
          <FmtValue>657</FmtValue>
          <FormatString>#,###</FormatString>
        </Cell>
        <Cell CellOrdinal="5">
          <Value xsi:type="xsd:double">6108.38</Value>
          <FmtValue>6.108,38</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="6">
          <Value xsi:type="xsd:double">12741.187</Value>
          <FmtValue>$12.741,19</FmtValue>
          <FormatString>$#,##0.00</FormatString>
        </Cell>
        <Cell CellOrdinal="7">
          <Value xsi:type="xsd:double">-0.14289748385006706</Value>
          <FmtValue>-14,3%</FmtValue>
          <FormatString>0.0%</FormatString>
        </Cell>
        <Cell CellOrdinal="8">
          <Value xsi:type="xsd:double">14865.4178</Value>
          <FmtValue>$14.865,42</FmtValue>
          <FormatString>$#,##0.00</FormatString>
        </Cell>
        <Cell CellOrdinal="9">
          <Value xsi:type="xsd:double">10536</Value>
          <FmtValue>10.536</FmtValue>
          <FormatString>Standard</FormatString>
        </Cell>
        <Cell CellOrdinal="10">
          <Value xsi:type="xsd:double">8862.9146</Value>
          <FmtValue>8.862,91</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="11">
          <Value xsi:type="xsd:double">22200.18</Value>
          <FmtValue>22.200,18</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="12">
          <Value xsi:type="xsd:int">3438</Value>
          <FmtValue>3.438</FmtValue>
          <FormatString>#,###</FormatString>
        </Cell>
        <Cell CellOrdinal="13">
          <Value xsi:type="xsd:int">672</Value>
          <FmtValue>672</FmtValue>
          <FormatString>#,###</FormatString>
        </Cell>
        <Cell CellOrdinal="14">
          <Value xsi:type="xsd:double">4695.4</Value>
          <FmtValue>4.695,40</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="15">
          <Value xsi:type="xsd:double">13337.2654</Value>
          <FmtValue>$13.337,27</FmtValue>
          <FormatString>$#,##0.00</FormatString>
        </Cell>
        <Cell CellOrdinal="16">
          <Value xsi:type="xsd:double">0.04678358460636362</Value>
          <FmtValue>4,7%</FmtValue>
          <FormatString>0.0%</FormatString>
        </Cell>
        <Cell CellOrdinal="17">
          <Value xsi:type="xsd:double">12741.187</Value>
          <FmtValue>$12.741,19</FmtValue>
          <FormatString>$#,##0.00</FormatString>
        </Cell>
        <Cell CellOrdinal="18">
          <Value xsi:type="xsd:double">10466</Value>
          <FmtValue>10.466</FmtValue>
          <FormatString>Standard</FormatString>
        </Cell>
        <Cell CellOrdinal="19">
          <Value xsi:type="xsd:double">8977.7991</Value>
          <FmtValue>8.977,80</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="20">
          <Value xsi:type="xsd:double">22446.91</Value>
          <FmtValue>22.446,91</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="21">
          <Value xsi:type="xsd:int">3388</Value>
          <FmtValue>3.388</FmtValue>
          <FormatString>#,###</FormatString>
        </Cell>
        <Cell CellOrdinal="22">
          <Value xsi:type="xsd:int">650</Value>
          <FmtValue>650</FmtValue>
          <FormatString>#,###</FormatString>
        </Cell>
        <Cell CellOrdinal="23">
          <Value xsi:type="xsd:double">6606.76</Value>
          <FmtValue>6.606,76</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="24">
          <Value xsi:type="xsd:double">13469.1109</Value>
          <FmtValue>$13.469,11</FmtValue>
          <FormatString>$#,##0.00</FormatString>
        </Cell>
        <Cell CellOrdinal="25">
          <Value xsi:type="xsd:double">0.009885497217443048</Value>
          <FmtValue>1,0%</FmtValue>
          <FormatString>0.0%</FormatString>
        </Cell>
        <Cell CellOrdinal="26">
          <Value xsi:type="xsd:double">13337.2654</Value>
          <FmtValue>$13.337,27</FmtValue>
          <FormatString>$#,##0.00</FormatString>
        </Cell>
        <Cell CellOrdinal="27">
          <Value xsi:type="xsd:double">10189</Value>
          <FmtValue>10.189</FmtValue>
          <FormatString>Standard</FormatString>
        </Cell>
        <Cell CellOrdinal="28">
          <Value xsi:type="xsd:double">8642.8363</Value>
          <FmtValue>8.642,84</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="29">
          <Value xsi:type="xsd:double">21668.2</Value>
          <FmtValue>21.668,20</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="30">
          <Value xsi:type="xsd:int">3339</Value>
          <FmtValue>3.339</FmtValue>
          <FormatString>#,###</FormatString>
        </Cell>
        <Cell CellOrdinal="31">
          <Value xsi:type="xsd:int">660</Value>
          <FmtValue>660</FmtValue>
          <FormatString>#,###</FormatString>
        </Cell>
        <Cell CellOrdinal="32">
          <Value xsi:type="xsd:double">5196</Value>
          <FmtValue>5.196,00</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="33">
          <Value xsi:type="xsd:double">13025.3637</Value>
          <FmtValue>$13.025,36</FmtValue>
          <FormatString>$#,##0.00</FormatString>
        </Cell>
        <Cell CellOrdinal="34">
          <Value xsi:type="xsd:double">-0.14252509703003943</Value>
          <FmtValue>-14,3%</FmtValue>
          <FormatString>0.0%</FormatString>
        </Cell>
        <Cell CellOrdinal="35">
          <Value xsi:type="xsd:double">15190.3731</Value>
          <FmtValue>$15.190,37</FmtValue>
          <FormatString>$#,##0.00</FormatString>
        </Cell>
        <Cell CellOrdinal="36">
          <Value xsi:type="xsd:double">10545</Value>
          <FmtValue>10.545</FmtValue>
          <FormatString>Standard</FormatString>
        </Cell>
        <Cell CellOrdinal="37">
          <Value xsi:type="xsd:double">8919.6411</Value>
          <FmtValue>8.919,64</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="38">
          <Value xsi:type="xsd:double">22256.11</Value>
          <FmtValue>22.256,11</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="39">
          <Value xsi:type="xsd:int">3428</Value>
          <FmtValue>3.428</FmtValue>
          <FormatString>#,###</FormatString>
        </Cell>
        <Cell CellOrdinal="40">
          <Value xsi:type="xsd:int">699</Value>
          <FmtValue>699</FmtValue>
          <FormatString>#,###</FormatString>
        </Cell>
        <Cell CellOrdinal="41">
          <Value xsi:type="xsd:double">4906.08</Value>
          <FmtValue>4.906,08</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="42">
          <Value xsi:type="xsd:double">13336.4689</Value>
          <FmtValue>$13.336,47</FmtValue>
          <FormatString>$#,##0.00</FormatString>
        </Cell>
        <Cell CellOrdinal="43">
          <Value xsi:type="xsd:double">0.023884569150264878</Value>
          <FmtValue>2,4%</FmtValue>
          <FormatString>0.0%</FormatString>
        </Cell>
        <Cell CellOrdinal="44">
          <Value xsi:type="xsd:double">13025.3637</Value>
          <FmtValue>$13.025,36</FmtValue>
          <FormatString>$#,##0.00</FormatString>
        </Cell>
        <Cell CellOrdinal="45">
          <Value xsi:type="xsd:double">10884</Value>
          <FmtValue>10.884</FmtValue>
          <FormatString>Standard</FormatString>
        </Cell>
        <Cell CellOrdinal="46">
          <Value xsi:type="xsd:double">9092.1707</Value>
          <FmtValue>9.092,17</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="47">
          <Value xsi:type="xsd:double">22884.82</Value>
          <FmtValue>22.884,82</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="48">
          <Value xsi:type="xsd:int">3524</Value>
          <FmtValue>3.524</FmtValue>
          <FormatString>#,###</FormatString>
        </Cell>
        <Cell CellOrdinal="49">
          <Value xsi:type="xsd:int">686</Value>
          <FmtValue>686</FmtValue>
          <FormatString>#,###</FormatString>
        </Cell>
        <Cell CellOrdinal="50">
          <Value xsi:type="xsd:double">6318.56</Value>
          <FmtValue>6.318,56</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="51">
          <Value xsi:type="xsd:double">13792.6493</Value>
          <FmtValue>$13.792,65</FmtValue>
          <FormatString>$#,##0.00</FormatString>
        </Cell>
        <Cell CellOrdinal="52">
          <Value xsi:type="xsd:double">0.03420548598137542</Value>
          <FmtValue>3,4%</FmtValue>
          <FormatString>0.0%</FormatString>
        </Cell>
        <Cell CellOrdinal="53">
          <Value xsi:type="xsd:double">13336.4689</Value>
          <FmtValue>$13.336,47</FmtValue>
          <FormatString>$#,##0.00</FormatString>
        </Cell>
      </CellData>
    </root>
  </cxmla:return>
</cxmla:ExecuteResponse>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""),
    ],
    "testNoAxesButOneCell":[
        ("request", """<soap-env:Envelope xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/" xmlns="urn:schemas-microsoft-com:xml-analysis">
  <soap-env:Body>
    <Execute>
      <Command>
        <Statement>select from [Sales]</Statement>
      </Command>
      <Properties>
        <PropertyList>
          <Format>Multidimensional</Format>
          <AxisFormat>TupleFormat</AxisFormat>
          <Catalog>FoodMart</Catalog>
        </PropertyList>
      </Properties>
    </Execute>
  </soap-env:Body>
</soap-env:Envelope>
"""),
        ("response", """<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
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
          <AxisInfo name="SlicerAxis"/>
        </AxesInfo>
        <CellInfo>
          <Value name="VALUE"/>
          <FmtValue name="FORMATTED_VALUE"/>
          <FormatString name="FORMAT_STRING"/>
        </CellInfo>
      </OlapInfo>
      <Axes>
        <Axis name="SlicerAxis">
          <Tuples>
            <Tuple/>
          </Tuples>
        </Axis>
      </Axes>
      <CellData>
        <Cell CellOrdinal="0">
          <Value xsi:type="xsd:double">266773</Value>
          <FmtValue>266.773</FmtValue>
          <FormatString>Standard</FormatString>
        </Cell>
      </CellData>
    </root>
  </cxmla:return>
</cxmla:ExecuteResponse>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""),
    ],
    "testOneDimensional":[
        ("request", """<soap-env:Envelope xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/" xmlns="urn:schemas-microsoft-com:xml-analysis">
  <soap-env:Body>
    <Execute>
      <Command>
        <Statement>select [Measures].ALLMEMBERS on columns from [Sales]</Statement>
      </Command>
      <Properties>
        <PropertyList>
          <Format>Multidimensional</Format>
          <AxisFormat>TupleFormat</AxisFormat>
          <Catalog>FoodMart</Catalog>
        </PropertyList>
      </Properties>
    </Execute>
  </soap-env:Body>
</soap-env:Envelope>
"""),
        ("response", """<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
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
                <UName>[Measures].[Unit Sales]</UName>
                <Caption>Unit Sales</Caption>
                <LName>[Measures].[MeasuresLevel]</LName>
                <LNum>0</LNum>
                <DisplayInfo>0</DisplayInfo>
              </Member>
            </Tuple>
            <Tuple>
              <Member Hierarchy="Measures">
                <UName>[Measures].[Store Cost]</UName>
                <Caption>Store Cost</Caption>
                <LName>[Measures].[MeasuresLevel]</LName>
                <LNum>0</LNum>
                <DisplayInfo>0</DisplayInfo>
              </Member>
            </Tuple>
            <Tuple>
              <Member Hierarchy="Measures">
                <UName>[Measures].[Store Sales]</UName>
                <Caption>Store Sales</Caption>
                <LName>[Measures].[MeasuresLevel]</LName>
                <LNum>0</LNum>
                <DisplayInfo>0</DisplayInfo>
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
            </Tuple>
            <Tuple>
              <Member Hierarchy="Measures">
                <UName>[Measures].[Customer Count]</UName>
                <Caption>Customer Count</Caption>
                <LName>[Measures].[MeasuresLevel]</LName>
                <LNum>0</LNum>
                <DisplayInfo>0</DisplayInfo>
              </Member>
            </Tuple>
            <Tuple>
              <Member Hierarchy="Measures">
                <UName>[Measures].[Promotion Sales]</UName>
                <Caption>Promotion Sales</Caption>
                <LName>[Measures].[MeasuresLevel]</LName>
                <LNum>0</LNum>
                <DisplayInfo>0</DisplayInfo>
              </Member>
            </Tuple>
            <Tuple>
              <Member Hierarchy="Measures">
                <UName>[Measures].[Profit]</UName>
                <Caption>Profit</Caption>
                <LName>[Measures].[MeasuresLevel]</LName>
                <LNum>0</LNum>
                <DisplayInfo>0</DisplayInfo>
              </Member>
            </Tuple>
            <Tuple>
              <Member Hierarchy="Measures">
                <UName>[Measures].[Profit Growth]</UName>
                <Caption>Gewinn-Wachstum</Caption>
                <LName>[Measures].[MeasuresLevel]</LName>
                <LNum>0</LNum>
                <DisplayInfo>0</DisplayInfo>
              </Member>
            </Tuple>
            <Tuple>
              <Member Hierarchy="Measures">
                <UName>[Measures].[Profit last Period]</UName>
                <Caption>Profit last Period</Caption>
                <LName>[Measures].[MeasuresLevel]</LName>
                <LNum>0</LNum>
                <DisplayInfo>0</DisplayInfo>
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
          <Value xsi:type="xsd:double">266773</Value>
          <FmtValue>266.773</FmtValue>
          <FormatString>Standard</FormatString>
        </Cell>
        <Cell CellOrdinal="1">
          <Value xsi:type="xsd:double">225627.2336</Value>
          <FmtValue>225.627,23</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="2">
          <Value xsi:type="xsd:double">565238.13</Value>
          <FmtValue>565.238,13</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="3">
          <Value xsi:type="xsd:int">86837</Value>
          <FmtValue>86.837</FmtValue>
          <FormatString>#,###</FormatString>
        </Cell>
        <Cell CellOrdinal="4">
          <Value xsi:type="xsd:int">5581</Value>
          <FmtValue>5.581</FmtValue>
          <FormatString>#,###</FormatString>
        </Cell>
        <Cell CellOrdinal="5">
          <Value xsi:type="xsd:double">151211.21</Value>
          <FmtValue>151.211,21</FmtValue>
          <FormatString>#,###.00</FormatString>
        </Cell>
        <Cell CellOrdinal="6">
          <Value xsi:type="xsd:double">339610.89639999997</Value>
          <FmtValue>$339.610,90</FmtValue>
          <FormatString>$#,##0.00</FormatString>
        </Cell>
        <Cell CellOrdinal="7">
          <Value xsi:type="xsd:double">0</Value>
          <FmtValue>0,0%</FmtValue>
          <FormatString>0.0%</FormatString>
        </Cell>
        <Cell CellOrdinal="8">
          <Value xsi:type="xsd:double">339610.89639999997</Value>
          <FmtValue>$339.610,90</FmtValue>
          <FormatString>$#,##0.00</FormatString>
        </Cell>
      </CellData>
    </root>
  </cxmla:return>
</cxmla:ExecuteResponse>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""),
    ],
}