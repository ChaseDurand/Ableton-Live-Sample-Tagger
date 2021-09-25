# Valid hex, sample on root
hexInput1 = (
    '00000000029600020000064D41435353440000000000000000000000000000000000000000000000000042440001FFFFFFFF1F4261636B77617264732038382042504D20422346464646464646462E7761760000000000000000000000000000000000000000000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF00000A20637500000000000000000000000000075265766572736500000200A32F3A55736572733A6368617365647572616E643A417564696F2050726F64756374696F6E3A41626C65746F6E4C69766550726F6A656374733A64726F7020746F702050726F6A6563743A53616D706C65733A50726F6365737365643A526576657273653A4261636B77617264732038382042504D20426D696E20284465787465722057616E73656C202D20546865205377656574657374205061696E2920522E77617600000E0080003F004200610063006B00770061007200640073002000380038002000420050004D00200042006D0069006E00200028004400650078007400650072002000570061006E00730065006C0020002D00200054006800650020005300770065006500740065007300740020005000610069006E002900200052002E007700610076000F000E0006004D00410043005300530044001200A155736572732F6368617365647572616E642F417564696F2050726F64756374696F6E2F41626C65746F6E4C69766550726F6A656374732F64726F7020746F702050726F6A6563742F53616D706C65732F50726F6365737365642F526576657273652F4261636B77617264732038382042504D20426D696E20284465787465722057616E73656C202D20546865205377656574657374205061696E2920522E77617600001300012F00001500020012FFFF0000',
    '/Users/chasedurand/Audio Production/AbletonLiveProjects/drop top Project/Samples/Processed/Reverse/Backwards 88 BPM Bmin (Dexter Wansel - The Sweetest Pain) R.wav'
)

# Invalid hex (incorrect length)
hexInput2 = (
    '0000000002F600020000064D41435353440000000000000000000000000000000000000000000000000042440001FFFFFFFF1F4261636B77617264732038382042504D20422346464646464646462E7761760000000000000000000000000000000000000000000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF00000A20637500000000000000000000000000075265766572736500000200A32F3A55736572733A6368617365647572616E643A417564696F2050726F64756374696F6E3A41626C65746F6E4C69766550726F6A656374733A64726F7020746F702050726F6A6563743A53616D706C65733A50726F6365737365643A526576657273653A4261636B77617264732038382042504D20426D696E20284465787465722057616E73656C202D20546865205377656574657374205061696E2920522E77617600000E0080003F004200610063006B00770061007200640073002000380038002000420050004D00200042006D0069006E00200028004400650078007400650072002000570061006E00730065006C0020002D00200054006800650020005300770065006500740065007300740020005000610069006E002900200052002E007700610076000F000E0006004D00410043005300530044001200A155736572732F6368617365647572616E642F417564696F2050726F64756374696F6E2F41626C65746F6E4C69766550726F6A656374732F64726F7020746F702050726F6A6563742F53616D706C65732F50726F6365737365642F526576657273652F4261636B77617264732038382042504D20426D696E20284465787465722057616E73656C202D20546865205377656574657374205061696E2920522E77617600001300012F00001500020012FFFF0000',
    '')

# Invalid hex (incorrect length)
hexInput3 = ('00000000029600020000064D41435357FFFF0000', '')