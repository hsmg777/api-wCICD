def createApp(testing=False):
    app = Flask(__name__)
    
    # Configuración general
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "ToDoList API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # Configuración de la base de datos
    if testing:
        # Usar SQLite en memoria para pruebas
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    else:
        # Usar MSSQLLocalDB en modo normal
        server = '(localdb)\\MSSQLLocalDB'
        database = 'ToDoList'
        username = 'aurora'
        password = 'mamifer1'
        driver = 'ODBC Driver 17 for SQL Server'
        
        params = urllib.parse.quote_plus(
            f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
        )
        connection_string = f"mssql+pyodbc:///?odbc_connect={params}"
        app.config['SQLALCHEMY_DATABASE_URI'] = connection_string

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa la base de datos con la aplicación
    init_db(app)
    
    # Configurar CORS
    CORS(app)
    
    # Configurar API con Flask-Smorest
    api = Api(app)
    
    # Registrar el blueprint
    api.register_blueprint(TareaBluePrint)
   
    return app
