/* Config Sample
 *
 * For more information on how you can configure this file
 * see https://docs.magicmirror.builders/configuration/introduction.html
 * and https://docs.magicmirror.builders/modules/configuration.html
 *
 * You can use environment variables using a `config.js.template` file instead of `config.js`
 * which will be converted to `config.js` while starting. For more information
 * see https://docs.magicmirror.builders/configuration/introduction.html#enviromnent-variables
 */
let config = {
	address: "localhost",	// Address to listen on, can be:
	// - "localhost", "127.0.0.1", "::1" to listen on loopback interface
	// - another specific IPv4/6 to listen on a specific interface
	// - "0.0.0.0", "::" to listen on any interface
	// Default, when address config is left out or empty, is "localhost"
	port: 8080,
	basePath: "/",	// The URL path where MagicMirror² is hosted. If you are using a Reverse proxy
	// you must set the sub path here. basePath must end with a /
	ipWhitelist: [],	// Set [] to allow all IP addresses
	//ipWhitelist: ["127.0.0.1", "::ffff:127.0.0.1", "::1"],	// Set [] to allow all IP addresses
	// or add a specific IPv4 of 192.168.1.5 :
	// ["127.0.0.1", "::ffff:127.0.0.1", "::1", "::ffff:192.168.1.5"],
	// or IPv4 range of 192.168.3.0 --> 192.168.3.15 use CIDR format :
	// ["127.0.0.1", "::ffff:127.0.0.1", "::1", "::ffff:192.168.3.0/28"],

	useHttps: false,			// Support HTTPS or not, default "false" will use HTTP
	httpsPrivateKey: "",	// HTTPS private key path, only require when useHttps is true
	httpsCertificate: "",	// HTTPS Certificate path, only require when useHttps is true

	language: "en",
	locale: "en-US",   // this variable is provided as a consistent location
	// it is currently only used by 3rd party modules. no MagicMirror code uses this value
	// as we have no usage, we  have no constraints on what this field holds
	// see https://en.wikipedia.org/wiki/Locale_(computer_software) for the possibilities

	logLevel: ["INFO", "LOG", "WARN", "ERROR"], // Add "DEBUG" for even more logging
	timeFormat: 12,
	units: "metric",

	modules: [
		{
			module: "alert",
		},
		{
			module: "updatenotification",
			position: "top_bar"
		},
		{
			module: "clock",
			position: "top_left"
		},
		{
			module: "calendar",
			header: "SG Holidays",
			position: "top_right",
			config: {
				calendars: [
					{
						fetchInterval: 7 * 24 * 60 * 60 * 1000,
						symbol: "calendar-check",
						url: "https://www.mom.gov.sg/-/media/mom/documents/employment-practices/public-holidays/public-holidays-sg-2025.ics"
					}
				]
			}
		},
		{
			module: 'MMM-MQTT',
			position: 'top_left',
			header: 'Greeting',
			config: {
				logging: false,
				useWildcards: false,
				bigMode: false, // Set to true to display big numbers with label above
				mqttServers: [
					{
						address: '0.0.0.0',  // Server address or IP address
						port: '1883',          // Port number if other than default
						// ca: '/path/to/ca/cert.crt', // Path to trusted CA certificate file (optional)
						// cert: '/path/to/cert/cert.crt', // Path to cert certificate file (optional)
						// key: '/path/to/key/private.key', // Path to private key file (optional)
						// allowUnauthorized: true, // Allow unauthorized connections for self signed certificates (optional)
						// clientId: 'mirror',     // Custom MQTT client ID (optional)
						// user: 'user',          // Leave out for no user
						// password: 'password',      // Leave out for no password
						subscriptions: [
							{
								topic: 'greet', // Topic to look for
								label: '', // Displayed in front of value
							},
						]
					}
				],
			}
		},
		{
			module: "calendar",
			header: "Schedule",
			position: "top_left",
			config: {
				calendars: [
					{
						fetchInterval: 60000,
						symbol: "calendar-check",
						url: "http://192.168.153.1:5000/schedule"
					}
				]
			}
		},
		// {
		// 	module: "compliments",
		// 	position: "lower_third"
		// },
		// {
		// 	module: "weather",
		// 	position: "top_right",
		// 	config: {
		// 		weatherProvider: "openmeteo",
		// 		type: "current",
		// 		lat: 1.43105461806496,
		// 		lon: 103.83629956663546
		// 	}
		// },
		{
			module: "weather",
			position: "top_right",
			header: "Weather Forecast",
			config: {
				weatherProvider: "openmeteo",
				type: "forecast",
				lat: 1.43105461806496,
				lon: 103.83629956663546
			}
		},
		// {
		// 	module: "newsfeed",
		// 	position: "bottom_bar",
		// 	config: {
		// 		feeds: [
		// 			{
		// 				title: "New York Times",
		// 				url: "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"
		// 			}
		// 		],
		// 		showSourceTitle: true,
		// 		showPublishDate: true,
		// 		broadcastNewsFeeds: true,
		// 		broadcastNewsUpdates: true
		// 	}
		// },
		// {
		// 	module: 'MMM-MQTT',
		// 	position: 'bottom_left',
		// 	header: 'MQTT',
		// 	config: {
		// 		logging: false,
		// 		useWildcards: false,
		// 		bigMode: false, // Set to true to display big numbers with label above
		// 		mqttServers: [
		// 			{
		// 				address: '192.168.153.1',  // Server address or IP address
		// 				port: '1883',          // Port number if other than default
		// 				// ca: '/path/to/ca/cert.crt', // Path to trusted CA certificate file (optional)
		// 				// cert: '/path/to/cert/cert.crt', // Path to cert certificate file (optional)
		// 				// key: '/path/to/key/private.key', // Path to private key file (optional)
		// 				// allowUnauthorized: true, // Allow unauthorized connections for self signed certificates (optional)
		// 				// clientId: 'mirror',     // Custom MQTT client ID (optional)
		// 				// user: 'user',          // Leave out for no user
		// 				// password: 'password',      // Leave out for no password
		// 				subscriptions: [
		// 					{
		// 						topic: 'smoky/1/inside/temperature', // Topic to look for
		// 						label: 'Temperature', // Displayed in front of value
		// 						suffix: '°C',         // Displayed after the value
		// 						decimals: 1,          // Round numbers to this number of decimals
		// 						sortOrder: 10,        // Can be used to sort entries in the same table
		// 						maxAgeSeconds: 60,    // Reduce intensity if value is older
		// 						broadcast: true,      // Broadcast messages to other modules
		// 						colors: [             // Value dependent colors
		// 							{ upTo: -10, value: "blue", label: "blue", suffix: "blue" },
		// 							{ upTo: 0, value: "#00ccff", label: "#00ccff", suffix: "#00ccff" },
		// 							{ upTo: 10, value: "yellow" },
		// 							{ upTo: 25, label: "green", suffix: "green" },
		// 							{ upTo: 100, label: "red" }, // The last one is used for higher values too
		// 						],
		// 					},
		// 					{
		// 						topic: 'smoky/1/inside/humidity',
		// 						label: 'Luftfuktighet',
		// 						suffix: '%',
		// 						decimals: 0,
		// 						sortOrder: 20,
		// 						maxAgeSeconds: 60
		// 					},
		// 					{
		// 						topic: 'smoky/2/inside/temperature',
		// 						label: 'Temp ute',
		// 						decimals: 1,
		// 						decimalSignInMessage: ",", // If the message decimal point is not "."
		// 						sortOrder: 20,
		// 						maxAgeSeconds: 60
		// 					},
		// 					{
		// 						topic: 'smoky/1/inside/smoke',
		// 						label: 'Røyk',
		// 						sortOrder: 30,
		// 						divide: 10, // Divide numeric values. Alternatively use `multiply`.
		// 						maxAgeSeconds: 60
		// 					},
		// 					{
		// 						topic: 'guests',
		// 						label: 'First guest',
		// 					},
		// 					{
		// 						topic: 'powerprices',
		// 						label: 'Power prices',
		// 						broadcast: true,
		// 						hidden: true    // Do not display in the table
		// 					},
		// 					{
		// 						topic: "house/1/doors/1",
		// 						label: "Door",
		// 						conversions: [
		// 							{ from: "true", to: "Open" },
		// 							{ from: "false", to: "Closed" }
		// 						]
		// 					}
		// 				]
		// 			}
		// 		],
		// 	}
		// },
		{
			module: 'MMM-MQTT',
			position: 'bottom_right',
			header: 'Health Metrics',
			config: {
				logging: false,
				useWildcards: false,
				bigMode: false, // Set to true to display big numbers with label above
				mqttServers: [
					{
						address: '0.0.0.0',  // Server address or IP address
						port: '1883',          // Port number if other than default
						// ca: '/path/to/ca/cert.crt', // Path to trusted CA certificate file (optional)
						// cert: '/path/to/cert/cert.crt', // Path to cert certificate file (optional)
						// key: '/path/to/key/private.key', // Path to private key file (optional)
						// allowUnauthorized: true, // Allow unauthorized connections for self signed certificates (optional)
						// clientId: 'mirror',     // Custom MQTT client ID (optional)
						// user: 'user',          // Leave out for no user
						// password: 'password',      // Leave out for no password
						subscriptions: [
							{
								topic: 'temperature', // Topic to look for
								label: 'Temp:', // Displayed in front of value
							},
							{
								topic: 'humidity', // Topic to look for
								label: 'Humidity:', // Displayed in front of value
							},
							{
								topic: 'heartrate', // Topic to look for
								label: 'Heart-Rate:', // Displayed in front of value
								suffix: 'bpm'
							},
							{
								topic: 'bodytemp', // Topic to look for
								label: 'Body Temp:', // Displayed in front of value
								suffix: '°C'
							},
						]
					}
				],
			}
		},
		{
			module: 'MMM-MQTT',
			position: 'bottom_left',
			header: 'name and age',
			hiddenOnStartup: true,
			config: {
				logging: false,
				useWildcards: false,
				bigMode: false, // Set to true to display big numbers with label above
				mqttServers: [
					{
						address: '0.0.0.0',  // Server address or IP address
						port: '1883',          // Port number if other than default
						// ca: '/path/to/ca/cert.crt', // Path to trusted CA certificate file (optional)
						// cert: '/path/to/cert/cert.crt', // Path to cert certificate file (optional)
						// key: '/path/to/key/private.key', // Path to private key file (optional)
						// allowUnauthorized: true, // Allow unauthorized connections for self signed certificates (optional)
						// clientId: 'mirror',     // Custom MQTT client ID (optional)
						// user: 'user',          // Leave out for no user
						// password: 'password',      // Leave out for no password
						subscriptions: [
							{
								topic: 'name', // Topic to look for
								label: 'Name:', // Displayed in front of value
							},
							{
								topic: 'age', // Topic to look for
								label: 'Age:', // Displayed in front of value
							},
							{
								topic: 'schedule', // Topic to look for
								label: 'Schedule:', // Displayed in front of value
								broadcast: true,
							},
						]
					}
				],
			}
		},
		// {
		// 	module: 'MMM-Response',
		// 	position: 'bottom_center'
		// },
		{
			module: 'MMM-MQTT',
			position: 'top_center',
			header: 'Response',
			config: {
				logging: false,
				useWildcards: false,
				bigMode: false, // Set to true to display big numbers with label above
				mqttServers: [
					{
						address: '0.0.0.0',  // Server address or IP address
						port: '1883',          // Port number if other than default
						// ca: '/path/to/ca/cert.crt', // Path to trusted CA certificate file (optional)
						// cert: '/path/to/cert/cert.crt', // Path to cert certificate file (optional)
						// key: '/path/to/key/private.key', // Path to private key file (optional)
						// allowUnauthorized: true, // Allow unauthorized connections for self signed certificates (optional)
						// clientId: 'mirror',     // Custom MQTT client ID (optional)
						// user: 'user',          // Leave out for no user
						// password: 'password',      // Leave out for no password
						subscriptions: [
							{
								topic: 'response', // Topic to look for
								label: '', // Displayed in front of value
							},
						]
					}
				],
			}
		},
	]
};

/*************** DO NOT EDIT THE LINE BELOW ***************/
if (typeof module !== "undefined") { module.exports = config; }
