<?php

require 'vendor/autoload.php';

use GuzzleHttp\Client;
use GuzzleHttp\Exception\RequestException;

$client = new Client();

$server1Url = getenv("SERVER1_URL");
$server2Url = getenv("SERVER2_URL");

$requestUri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
error_log('Request URI: ' . $requestUri);

if ($requestUri === '/all') {
    try {
        $server1Response = $client->request('GET', $server1Url);
        $server1Data = json_decode($server1Response->getBody(), true);

        $server2Response = $client->request('GET', $server2Url);
        $server2Data = json_decode($server2Response->getBody(), true);

        $combinedData = [];
        foreach ($server1Data as $author) {
            foreach ($server2Data as $book) {
                if ($author['authorId'] == $book['bookID']) {
                    $combinedData[] = [
                        'id' => $author['authorId'],
                        'author' => $author['authorName'],
                        'book' => $book['bookName'],
                    ];
                }
            }
        }

        header('Content-Type: application/json');
        echo json_encode($combinedData);

    } catch (RequestException $e) {
        http_response_code(500);
        echo json_encode([
            'error' => 'Failed to fetch data from one or more servers',
            'details' => $e->getMessage()
        ]);
    }
} else {
    http_response_code(404);
    echo json_encode(['error' => 'Not Found']);
}
