import request

def get_movie_details(title,api_key):
    url=f"http://www.omdbapi.com/?={title}&plot=full&apikey={api-key}"
    res = request.get(url).json()
    if res.get("Response")=="True":
        result=res.get("Plot","N/A"),res.get("Poster","N/A")
        plot=result[0]
        poster=result[1]
        return plot,poster

    return "N/A","N/A"