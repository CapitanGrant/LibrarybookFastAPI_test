class BaseEndpoint:
    response = None
    response_json = None

    def check_response_is_200(self):
        assert self.response.status == 200

    def check_response_is_400(self):
        assert self.response.status == 400

    def check_response_is_401(self):
        assert self.response.status == 401

    def check_response_is_403(self):
        assert self.response.status == 403

    def check_response_is_404(self):
        assert self.response.status == 404

    def check_response_is_409(self):
        assert self.response.status == 409
