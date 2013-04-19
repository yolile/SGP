from sqlalchemy import Column, Table
from sqlalchemy import Integer, String
from sqlalchemy.sql import select

def get_table(metadata):
    rolpermiso_table = Table(
                          'rolpermiso', metadata,
                          Column('idrol', Integer, primary_key=True),
                          Column('idpermiso', Integer, primary_key=True),
                          )
    return rolpermiso_table

class RolPermiso(object):
    def __init__(self, idrol,idpermiso):
        self.idrol = idrol
        self.idpermiso = idpermiso


    def __repr__(self):
        return "<RolPermiso '%s' '%s'>" % self.idrol, self.idpermiso