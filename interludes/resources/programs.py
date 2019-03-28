from flask_restful import Resource

from interludes.models import Program
from interludes.schema import program_schema, programs_schema


class ProgramResource(Resource):
    def get(self, program_id):
        program = Program.query.get(program_id)
        data = program_schema.dump(program).data
        return data


class ProgramListResource(Resource):
    def get(self):
        programs = Program.query.all()
        data = programs_schema.dump(programs).data
        return data
