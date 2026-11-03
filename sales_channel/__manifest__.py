{
    'name':'Sales Total Tax',
    'version': '12.0.1.0.3',
    'category': 'Accounting',
    'description':"""
    Avoids Order Line And Invoice Line Tax Calculations


    Instaed applies Tax Calucation to the Final Sales Values and Invoice Value

     """,
    'author':'Odoo Ninja',
    'depends':['base','sale','account'],
    'data':['views/sale_view.xml'

            ],
    'email':'odooninja@gmail.com',
    'application':True,
    'installable':True
}