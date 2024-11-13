from app import *


if __name__ == '__main__':
    # host = environ.get('MATHS_API_HOST')
    # port = environ.get('MATHS_API_PORT')
    # if not host:
    #     host = '0.0.0.0'
    # if not port:
    #     port = '5000'
    app.run(debug=True, threaded=True)

