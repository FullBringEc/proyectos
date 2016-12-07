# -*- encoding: utf-8 -*-
 
{
    "name": "SRIs2",
    "version": "1.0",
    "description": """
        Tablas
    """,
    "author": "Adrian Morales",
    "website": "",
    "category": "Tools",
    "depends": [
            "account",
            "base",
            "sri_modelos",
                ],
    "data":[
            "security/ir.model.access.csv",
            "sri_view.xml", #todos los archivos xml que posea nuestro modulo se debe de agregarse aqui
#			"data/codsustento_t5.xml",#"sri_tabla2_data.xml",
 #           "data/formapag_t16.xml",
  #          "data/pagolocext_t18.xml",
   #         "data/tipocomprobante_t4.xml",
    #        "data/tpidprov_t2.xml",
                            ],
    "demo_xml": [],
    "update_xml": [
           
                    ],
    "active": False,
    "installable": True,
    "certificate" : "",
}