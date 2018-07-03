import gmaps2geojson

writer = gmaps2geojson.Writer()
writer.query("2131 7th Ave, Seattle, WA 98121", "900 Poplar Pl S, Seattle, WA 98144")
writer.query("900 Poplar Pl S, Seattle, WA 98144", "219 Broadway E, Seattle, WA 98102")
writer.save("example.geojson")
