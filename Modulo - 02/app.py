import os.path
from flask import Flask
import os
import json
import run_backend
import time

app = Flask(__name__)

def get_predictions():

    videos = []
    path_site = os.path.realpath(os.path.dirname(__file__))
    novos_videos_json = os.path.join(path_site, 'novos_videos.json')

    if not os.path.exists(novos_videos_json):
        run_backend.update_db()

    last_update = os.path.getmtime(novos_videos_json) * 1e9

    if time.time_ns() - last_update > (720*3600*1e9): # aprox. 1 mes
        run_backend.update_db()

    with open(novos_videos_json, 'r', encoding='utf-8') as data_file:
        videos = json.load(data_file)

    predictions = []
    for video in videos:
        predictions.append((video['video_id'], video['title'], float(video['score'])))

    predictions = sorted(predictions, key=lambda x: x[2], reverse=True)[:30]
    predictions_formatted = []
    for e in predictions:
        predictions_formatted.append('<tr><th><a href=\"{link}\">{title}</a></th><th>{score}</th></tr>'.format(title=e[1], link=e[0], score=e[2]))
    
    return '\n'.join(predictions_formatted), last_update


@app.route('/')
def main_page():
    preds, last_update = get_predictions()
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
        <title>Recomendação de vídeos do YouTube</title>
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-light">
            <a class="navbar-brand text-body" href="https://github.com/Angelicogfa/EstudoDataScienceAvancado" target="_blank">Recomendador de vídeos do YouTube</a>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav mr-auto"></ul>
                <form class="form-inline my-2 my-lg-0">
                    <input class="form-control mr-sm-2" type="search" placeholder="Link do youtube" aria-label="Search">
                    <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Analisar</button>
                </form>
            </div>
        </nav>
        <div class="container container-fluid">
            <h1 class="title mt-4">Vídeos do Youtube</h1>
            </br>
            <p>Segundos desde a ultima atualização: <small>{atualizacao}</small></p>
            </br>
            <table class="table table-ligth">
                <thead>
                    <td>
                        Url
                    </td>
                    <td>
                        Score
                    </td>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
        <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
    </body>
    </html>
    """.format(atualizacao=(time.time_ns() - last_update) / 1e9, rows= preds)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
