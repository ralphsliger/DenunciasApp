from app import created_app
app = created_app(config='config')
app.run(host='0.0.0.0')