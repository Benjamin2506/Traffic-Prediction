let map;
let directionsService, directionsRenderer;

document.addEventListener('DOMContentLoaded', function () {
    async function initMap() {
        const { Map } = await google.maps.importLibrary("maps");

        map = new Map(document.getElementById("map"), {
            center: { lat: 21.083936319511885, lng: 79.17181215479515 },
            zoom: 8,
        });

        directionsService = new google.maps.DirectionsService();
        directionsRenderer = new google.maps.DirectionsRenderer();
        directionsRenderer.setMap(map);

        var onChangeHandler = function () {
            calculateAndDisplayRoute(directionsService, directionsRenderer);
        };
        document.getElementById('source').addEventListener('change', onChangeHandler);
        document.getElementById('destination').addEventListener('change', onChangeHandler);
    }

    function initAutocomplete() {
        var sourceInput = document.getElementById('source');
        var destinationInput = document.getElementById('destination');

        var autocompleteSource = new google.maps.places.Autocomplete(sourceInput);
        var autocompleteDestination = new google.maps.places.Autocomplete(destinationInput);
    }

    window.onload = initAutocomplete;

    function calculateAndDisplayRoute(directionsService, directionsRenderer) {
        directionsService.route(
            {
                origin: { query: document.getElementById('source').value },
                destination: { query: document.getElementById('destination').value },
                travelMode: google.maps.TravelMode.DRIVING
            },
            function (response, status) {
                if (status === 'OK') {
                    directionsRenderer.setDirections(response);
                } else {
                    window.alert('Directions request failed due to ' + status);
                }
            }
        );
    }

    function displayRoute(directionsJSON) {
        const parsedDirections = typeof directionsJSON === 'string'
            ? JSON.parse(directionsJSON)
            : directionsJSON;
        directionsRenderer.setDirections(parsedDirections);
    }

    $(document).ready(function () {
        $('#prediction-form').on('submit', function (event) {
            event.preventDefault();

            const source = $('#source').val();
            const destination = $('#destination').val();
            const vehicleType = $('#vehicle_type').val();
            const vehicleSpeed = $('#speed').val();

            $.ajax({
                type: 'POST',
                url: '/get_traffic_prediction',
                contentType: 'application/json',
                data: JSON.stringify({
                    source: source,
                    destination: destination,
                    vehicle_type: vehicleType,
                    vehicle_speed: vehicleSpeed
                }),
                success: function (response) {
                    if (response.error) {
                        alert(response.error);
                    } else {
                        $('#distance').text(response.distance);
                        $('#google_time').text(response.duration);
                        $('#predicted_time').text(response.predicted_time);
                        displayRoute(response.directions);
                    }
                },
                error: function (error) {
                    alert('Error: ' + error.responseText);
                }
            });
        });

        // Handle "Find Shortest Path" button
        $('#shortest-path-btn').on('click', function () {
            const source = $('#source').val();
            const destination = $('#destination').val();

            $.ajax({
                type: 'POST',
                url: '/get_shortest_path',
                contentType: 'application/json',
                data: JSON.stringify({
                    source: source,
                    destination: destination
                }),
                success: function (response) {
                    if (response.error) {
                        alert(response.error);
                    } else {
                        $('#distance').text(response.distance);
                        $('#google_time').text(response.duration);
                        $('#predicted_time').text(response.predicted_time);

                        calculateAndDisplayRoute(directionsService, directionsRenderer);
                    }
                },
                error: function (error) {
                    alert('Error: ' + error.responseText);
                }
            });
        });
    });

    initMap();
});
