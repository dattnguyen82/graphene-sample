import os
import graphene
import json

from flask import Flask
from flask import request
from flask_cors import cross_origin

from Database import database

import logging
logging.basicConfig()

app = Flask(__name__)

port = None
vcap = None

### Application Configuration
portStr = os.getenv("VCAP_APP_PORT")

if portStr is not None:
    port = int(portStr)

db = database()

### Rest Calls
@app.route("/rest/enterprises", methods=["GET"])
@cross_origin()
def get_enterprises():
    query = "SELECT * FROM gql_sample.enterprise"
    return db.get_json_from_query(query)

@app.route("/rest/enterprises/<enterprise_id>", methods=["GET"])
@cross_origin()
def get_enterprise_by_id(enterprise_id):
    query = "SELECT * FROM gql_sample.enterprise WHERE (id='" + str(enterprise_id) + "');"
    return db.get_json_from_query(query)

@app.route("/rest/enterprises/<enterprise_id>/sites", methods=["GET"])
@cross_origin()
def get_sites(enterprise_id):
    query = "SELECT * FROM gql_sample.site WHERE (enterprise_id='" + str(enterprise_id) + "');"
    return db.get_json_from_query(query)

@app.route("/rest/enterprises/<enterprise_id>/sites/<site_id>", methods=["GET"])
@cross_origin()
def get_site_by_id(enterprise_id,site_id):
    query = "SELECT * FROM gql_sample.site WHERE (id='" + str(site_id) + "' and enterprise_id='"+ str(enterprise_id)+"');"
    return db.get_json_from_query(query)

@app.route("/rest/enterprises/<enterprise_id>/sites/<site_id>/segments", methods=["GET"])
@cross_origin()
def get_segments(enterprise_id,site_id):
    query = "SELECT * FROM gql_sample.segment WHERE (site_id='" + str(site_id) + "');"
    return db.get_json_from_query(query)

@app.route("/rest/enterprises/<enterprise_id>/sites/<site_id>/segments/<segment_id>", methods=["GET"])
@cross_origin()
def get_segment_by_id(enterprise_id,site_id,segment_id):
    query = "SELECT * FROM gql_sample.segment WHERE (id='" + str(segment_id) + "');"
    return db.get_json_from_query(query)

@app.route("/rest/enterprises/<enterprise_id>/sites/<site_id>/segments/<segment_id>/assets", methods=["GET"])
@cross_origin()
def get_assets(enterprise_id,site_id,segment_id):
    query = "SELECT * FROM gql_sample.asset WHERE (segment_id='" + str(segment_id) + "');"
    return db.get_json_from_query(query)

@app.route("/rest/enterprises/<enterprise_id>/sites/<site_id>/segments/<segment_id>/assets/<asset_id>", methods=["GET"])
@cross_origin()
def get_assets_by_id(enterprise_id,site_id,segment_id,asset_id):
    query = "SELECT * FROM gql_sample.asset WHERE (id='" + str(asset_id) + "');"
    return db.get_json_from_query(query)
####



### GQL calls

class Asset(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    description = graphene.String()
    segment_id = graphene.Int()

    def map_from_row(self, row):
        self.id = row[0]
        self.name = row[1]
        self.description = row[2]
        self.segment_id = row[3]


class Segment(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    description = graphene.String()
    site_id = graphene.Int()
    assets = graphene.List(Asset)

    def resolve_assets(self, args, context, info):
        query = "SELECT * FROM gql_sample.asset WHERE(segment_id='" + str(self.id) + "')"
        rows = db.execute_query(query)
        results = []
        for row in rows:
            a = Asset()
            a.map_from_row(row)
            results.append(a)
        return results

    def map_from_row(self, row):
        self.id = row[0]
        self.name = row[1]
        self.description = row[2]
        self.site_id = row[3]


class Site(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    description = graphene.String()
    enterprise_id = graphene.Int()
    segments = graphene.List(Segment)
    assets = graphene.List(Asset)

    def resolve_segments(self, args, context, info):
        query = "SELECT * FROM gql_sample.segment WHERE(site_id='" + str(self.id) + "')"
        rows = db.execute_query(query)
        results = []
        for row in rows:
            a = Asset()
            a.map_from_row(row)
            results.append(a)
        return results

    def resolve_assets(self, args, context, info):
        query = "SELECT * FROM gql_sample.segment WHERE(site_id='" + str(self.id) + "')"
        segment_rows = db.execute_query(query)
        results = []
        for segment_row in segment_rows:
            segment_id = segment_row[0]
            query = "SELECT * FROM gql_sample.asset WHERE(segment_id='" + str(segment_id) + "')"
            rows = db.execute_query(query)
            for row in rows:
                a = Asset()
                a.map_from_row(row)
                results.append(a)
        return results

    def map_from_row(self, row):
        self.id = row[0]
        self.name = row[1]
        self.description = row[2]
        self.enterprise_id = row[3]


class Enterprise(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    description = graphene.String()
    sites = graphene.List(Site)
    segments = graphene.List(Segment)
    assets = graphene.List(Asset)

    def resolve_sites(self, args, context, info):
        query = "SELECT * FROM gql_sample.site WHERE(enterprise_id='" + str(self.id) + "')"
        rows = db.execute_query(query)
        results = []
        for row in rows:
            a = Site()
            a.map_from_row(row)
            results.append(a)
        return results

    def resolve_segments(self, args, context, info):
        query = "SELECT * FROM gql_sample.site WHERE(enterprise_id='" + str(self.id) + "')"
        site_rows = db.execute_query(query)
        results = []
        for site_row in site_rows:
            site_id = site_row[0]
            query = "SELECT * FROM gql_sample.segment WHERE(site_id='" + str(site_id) + "')"
            rows = db.execute_query(query)
            for row in rows:
                a = Segment()
                a.map_from_row(row)
                results.append(a)
        return results

    def resolve_assets(self, args, context, info):
        query = "SELECT * FROM gql_sample.site WHERE(enterprise_id='" + str(self.id) + "')"
        site_rows = db.execute_query(query)
        results = []
        for site_row in site_rows:
            site_id = site_row[0]
            query = "SELECT * FROM gql_sample.segment WHERE(site_id='" + str(site_id) + "')"
            segment_rows = db.execute_query(query)
            for segment_row in segment_rows:
                segment_id = segment_row[0]
                query = "SELECT * FROM gql_sample.asset WHERE(segment_id='" + str(segment_id) + "')"
                rows = db.execute_query(query)
                for row in rows:
                    a = Asset()
                    a.map_from_row(row)
                    results.append(a)
        return results

    def map_from_row(self, row):
        self.id = row[0]
        self.name = row[1]
        self.description = row[2]



class CreateEnterprise(graphene.Mutation):
    class Input:
        name = graphene.String()
        description = graphene.String()

        enterprise = graphene.Field(Enterprise)

    def mutate(self, args, context, info):
        name=args.get('name')
        description=args.get('description')
        query = "INSERT INTO gql_sample.asset(name, description) VALUES('"+name+"', '"+description+"')"
        rows = db.execute_query(query)
        print rows
        ret = Enterprise()
        row = [name, description]
        ret.map_from_row(row)
        return ret


class Query(graphene.ObjectType):
    asset = graphene.Field(Asset, id=graphene.Int())
    assets = graphene.List(Asset)

    segment = graphene.Field(Segment, id=graphene.Int())
    segments = graphene.List(Segment)

    site = graphene.Field(Site, id=graphene.Int())
    sites = graphene.List(Site)

    enterprise = graphene.Field(Enterprise, id=graphene.Int())
    enterprises = graphene.List(Enterprise)

    def resolve_assets(self, args, context, info):
        query = "SELECT * FROM gql_sample.asset"
        rows = db.execute_query(query)
        results = []
        for row in rows:
            a = Asset()
            a.map_from_row(row)
            results.append(a)
        return results

    def resolve_asset(self, args, context, info):
        id = args.get('id')
        query = "SELECT * FROM gql_sample.asset WHERE(id='"+str(id)+"')"
        rows = db.execute_query(query)
        results = []
        for row in rows:
            a = Asset()
            a.map_from_row(row)
            results.append(a)
        return results[0]

    def resolve_segments(self, args, context, info):
        query = "SELECT * FROM gql_sample.segment"
        rows = db.execute_query(query)
        results = []
        for row in rows:
            a = Segment()
            a.map_from_row(row)
            results.append(a)
        return results

    def resolve_segment(self, args, context, info):
        id = args.get('id')
        query = "SELECT * FROM gql_sample.segment WHERE(id='" + str(id) + "')"
        rows = db.execute_query(query)
        results = []
        for row in rows:
            a = Segment()
            a.map_from_row(row)
            results.append(a)
        return results[0]


    def resolve_sites(self, args, context, info):
        query = "SELECT * FROM gql_sample.site"
        rows = db.execute_query(query)
        results = []
        for row in rows:
            a = Site()
            a.map_from_row(row)
            results.append(a)
        return results

    def resolve_site(self, args, context, info):
        id = args.get('id')
        query = "SELECT * FROM gql_sample.site WHERE(id='" + str(id) + "')"
        rows = db.execute_query(query)
        results = []
        for row in rows:
            a = Site()
            a.map_from_row(row)
            results.append(a)
        return results[0]

    def resolve_enterprises(self, args, context, info):
        query = "SELECT * FROM gql_sample.enterprise"
        rows = db.execute_query(query)
        results = []
        for row in rows:
            a = Enterprise()
            a.map_from_row(row)
            results.append(a)
        return results

    def resolve_enterprise(self, args, context, info):
        id = args.get('id')
        query = "SELECT * FROM gql_sample.enterprise WHERE(id='" + str(id) + "')"
        rows = db.execute_query(query)
        results = []
        for row in rows:
            a = Enterprise()
            a.map_from_row(row)
            results.append(a)
        return results[0]

schema = graphene.Schema(query=Query)

print schema

@app.route("/gql/schema", methods=["GET"])
@cross_origin()
def gql_schema():
    return str(schema)
###

@app.route("/gql/query", methods=["POST"])
@cross_origin()
def gql_query():
    print request.data
    data = json.loads(request.data)
    query = data['query']
    args = data['args']
    print args
    print "[QUERY] - " + query
    vv = json.loads(args)
    # result = schema.execute(query, args)
    result = schema.execute(query, None, variable_values=vv)


    if len(result.errors) > 0:
        for error in result.errors:
            print "[ERROR] - " + str(error)

    return json.dumps(result.data)
###



### Main application
if __name__ == '__main__':
    if port is not None:
        app.run(host='0.0.0.0', port=port)
    else:
        app.run()