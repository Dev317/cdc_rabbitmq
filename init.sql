CREATE TABLE taxi_trip_aggregate (
	"VendorID" INTEGER, 
	aggregated_passenger_count INTEGER, 
	aggregated_trip_distance FLOAT(53), 
	aggregated_total_amount FLOAT(53)
);

INSERT INTO taxi_trip_aggregate VALUES
(1, 0.0, 0.0, 0.0),
(2, 0.0, 0.0, 0.0);
