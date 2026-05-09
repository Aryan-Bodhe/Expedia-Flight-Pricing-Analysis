import pandas as pd
import numpy as np

FLIGHT_DATA_PATH = "data/flights_clean_1gb.parquet"
AIRPORTS_DATA_PATH = "data/airportsData.csv"

class DataLoader:
    def __init__(self):
        self.flight_data = pd.read_parquet(FLIGHT_DATA_PATH)
        self.airport_data = pd.read_csv(AIRPORTS_DATA_PATH)

    def _get_flight_legs(self):

        dep = self.flight_data["segmentsDepartureAirportCodes"].explode().reset_index(drop=True)
        arr = self.flight_data["segmentsArrivalAirportCodes"].explode().reset_index(drop=True)

        legs = pd.DataFrame({"startingAirport": dep, "destinationAirport": arr}).dropna()
        return legs

    def get_airports(self):

        airports = self.airport_data.rename(columns={
            "AirportCode": "airport",
            "Lat": "lat",
            "Long": "lon"
        })

        legs = self._get_flight_legs()

        traffic = (
            legs["startingAirport"].value_counts() +
            legs["destinationAirport"].value_counts()
        ).reset_index()
        traffic.columns = ["airport", "traffic"]

        airports = airports.merge(traffic, on="airport", how="left")
        airports["traffic"] = airports["traffic"].fillna(0)
        airports["size"] = 5 + airports["traffic"] / 5000
        airports = airports[airports["traffic"] > 0]

        return airports
    

    def get_routes(self, filter_spaghetti=90):

        airports = self.get_airports()
        legs = self._get_flight_legs()

        routes = (
            legs.groupby(["startingAirport", "destinationAirport"])
                .size()
                .reset_index(name="count")
        )

        # Reduce spaghetti
        routes = routes[routes["count"] > filter_spaghetti]

        # -----------------------------
        # Merge coordinates
        # -----------------------------

        routes = routes.merge(
            airports[["airport", "lat", "lon"]],
            left_on="startingAirport", right_on="airport", how="left"
        )
        routes = routes.rename(columns={"lat": "start_lat", "lon": "start_lon"}).drop(columns=["airport"])

        routes = routes.merge(
            airports[["airport", "lat", "lon"]],
            left_on="destinationAirport", right_on="airport", how="left"
        )
        routes = routes.rename(columns={"lat": "end_lat", "lon": "end_lon"}).drop(columns=["airport"])


        nan_col = np.full(len(routes), None)
        lons = np.c_[routes["start_lon"].values, routes["end_lon"].values, nan_col].ravel()
        lats = np.c_[routes["start_lat"].values, routes["end_lat"].values, nan_col].ravel()

        return routes, lats, lons