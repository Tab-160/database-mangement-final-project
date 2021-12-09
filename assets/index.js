// Search functinality
/* Overview of what happens: 
User clicks "Search" on search.html
1. Client sends SQL to be run over Websocket to SocketServer on port 50002
2. SocketServer recives SQL
3. SocketServer runs runSQL()
4. SocketServer creates a HTML page called search-results.html
5. SocketServer sends Done to Client
6. Client gets redirected to /assets/search-results.html through HTTPServer
7. HTTPServer sends search-results.html over to Client
8. Client sends Done to SocketServer
9. SocketServer deletes search-results.html

This file will be implementing the Client side of this interaction
*/

function search(){
	
	// Get what the user wants to search for
    var search_term = document.getElementById('search_input_search').value;
	
	// Find radio button value
    var search_type = document.getElementsByName('type');

	// Sets up SQL request
	var sql = "SELECT name, retail_price, category, unit_vol FROM product WHERE ";
	
	// If the second button is selected, then search over category
	if(search_type[1].checked){
		sql += "category";
	} else {	// Otherwise, search over name
		sql += "name";
	}
	
	// Finish SQL
	sql += " LIKE '%" + search_term + "%'"
	
	

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "POST", '127.0.0.1:50001', false ); // false for synchronous request
    xmlHttp.send( sql );

}

// WebSocket approach
function searchWebSocket(){    
    // Set up websocket to communicate with SocketServer
    // TODO: get search_SQL set up properly
    var webSocket = new WebSocket("ws://localhost:50002");

    // Get what the user wants to search for
    var search_term = document.getElementById('search_input_search').value;

    // Set up the SQL to be sent properly
    var enc = new TextEncoder(); // always utf-8
    var search_SQL = "1";
    
    //var search_SQL = JSON.stringify("SELECT * FROM users");
	
	// Wait until Done message is sent
    webSocket.onmessage = function (event) {
        console.log(event.data);
    }
    
    console.log(search_SQL);
    
    // Tell SocketServer the search term once open
    webSocket.onopen = function (event) {
        console.log("35");
        webSocket.send(search_SQL);
        console.log("37");
    };
    
	while(true){
		if(webSocket.readyState == 1){
			webSocket.send(search_SQL);
			console.log("Message sent");
		} else {
			//console.log("Not open yet");
		}
	}
	
    
    
    //window.location.href = 'search_results.html';
    
    webSocket.close();
}