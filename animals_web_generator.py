import data_fetcher

from flask import Flask, request, render_template_string

app = Flask(__name__)


def serialize_animal(animal_obj):
    """
    Serializes an animal object into an HTML list item.

    Args:
        animal_obj (dict): A dictionary containing animal data (name, diet, locations, type).

    Returns:
        str: An HTML string representing the animal as a list item.
    """
    output = '<li class="cards__item">\n'
    output += f'  <div class="card__title">{animal_obj["name"]}</div>\n'
    output += '  <p class="card__text">\n'
    output += f'    <strong>Diet:</strong> {animal_obj["diet"]}<br/>\n'
    output += f'    <strong>Location:</strong> {", ".join(animal_obj["locations"])}<br/>\n'
    output += f'    <strong>Type:</strong> {animal_obj["type"]}<br/>\n'
    if 'skin_type' in animal_obj:
        output += f'    <strong>Skin Type:</strong> {animal_obj["skin_type"]}<br/>\n'  # Use skin_type if it exists
    output += '  </p>\n'
    output += '</li>\n'
    return output


@app.route('/', methods=['GET', 'POST'])
def index():
    animal_name = ""
    animals_html = ""
    error_message = ""

    if request.method == 'POST':
        animal_name = request.form.get('animal_name', '').strip()

        if animal_name:
            animals_data = data_fetcher.fetch_data(animal_name) # Call data_fetcher

            if animals_data:
                structured_data = []
                for animal in animals_data:
                    structured_data.append({
                        "name": animal.get("name", "Unknown"),
                        "diet": animal.get("characteristics", {}).get("diet", "Unknown"),  # Access diet from characteristics
                        "locations": animal.get("locations", []),
                        "type": animal.get("taxonomy", {}).get("class", "Unknown"),
                        "skin_type": animal.get("characteristics", {}).get("skin_type", "Unknown")
                    })

                for animal_obj in structured_data:
                    animals_html += serialize_animal(animal_obj)
            else:
                error_message = f'The animal "{animal_name}" doesn\'t exist.'

    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Animals</title>
        <style>
            @gray-darker:               #444444;
            @gray-dark:                 #696969;
            @gray:                      #999999;
            @gray-light:                #cccccc;
            @gray-lighter:              #ececec;
            @gray-lightest:             lighten(@gray-lighter,4%);


            html {
              background-color: #ffe9e9;
            }

            h1 {
                text-align: center;
                font-size: 40pt;
                font-weight: normal;
            }

            body {
              font-family: 'Roboto','Helvetica Neue', Helvetica, Arial, sans-serif;
              font-style: normal;
              font-weight: 400;
              letter-spacing: 0;
              padding: 1rem;
              text-rendering: optimizeLegibility;
              -webkit-font-smoothing: antialiased;
              -moz-osx-font-smoothing: grayscale;
              -moz-font-feature-settings: "liga" on;
              width: 900px;
              margin: auto;
            }

            .cards {
              list-style: none;
              margin: 0;
              padding: 0;
              display: flex; /* Add flexbox for horizontal layout */
              flex-wrap: wrap; /* Allow cards to wrap to the next line */
            }

            .cards__item {
              background-color: white;
              border-radius: 0.25rem;
              box-shadow: 0 20px 40px -14px rgba(0,0,0,0.25);
              overflow: hidden;
              padding: 1rem;
              margin: 1rem; /* Reduced margin for better spacing */
              width: calc(33.333% - 2rem); /* Adjust width for 3 cards per row */
              box-sizing: border-box; /* Include padding and border in the element's total width and height */
            }

            .card__title {
              color: @gray-dark;
              font-size: 1.25rem;
              font-weight: 300;
              letter-spacing: 2px;
              text-transform: uppercase;
            }

            .card__text {
              flex: 1 1 auto;
              font-size: 0.95rem;
              line-height: 2;
              margin-bottom: 0.25rem; /* Reduced margin for better spacing */
            }
            </style>
        </head>
        <body>
            <h1>Animal Information</h1>
            <form method="post">
                <label for="animal_name">Enter animal name:</label>
                <input type="text" id="animal_name" name="animal_name">
                <button type="submit">Search</button>
            </form>
            {% if error_message %}
                <h2>{{ error_message }}</h2>
            {% else %}
                <ul class="cards">
                    {{ animals_html|safe }}
                </ul>
            {% endif %}
        </body>
    </html>
    """

    return render_template_string(template, animal_name=animal_name, animals_html=animals_html, error_message=error_message)


if __name__ == '__main__':
    app.run(debug=True) # Turn debug to false in production.