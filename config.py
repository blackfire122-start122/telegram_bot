TOKEN = "Tocken"

Welcome = """
Hi I'm ShopList bot. 
For more details send:
/help
"""

Help = """
It bot show list shop their are 3: 
Show Necerrasy,
Show Need,
Show Unimportant

Show All
"""

Not_login = """
your not login send:
/start
"""

Get_name_shop = """
Shop name
"""

types_shop = [
	"Necerrasy",
	"Need",
	"Unimportant",
]

add_types_shop = {"Add "+i:i for i in types_shop}
show_type_shop = {"Show "+i:i for i in types_shop}
show_type_shop["Show All"]="*"