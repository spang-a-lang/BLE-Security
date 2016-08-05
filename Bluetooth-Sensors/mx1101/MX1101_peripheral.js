/*
 * Filename: MX1101_peripheral.js
 * Author: @spang
 *
 * Peripheral file for the Onset MX1101 data logger
 * for use with bleno (github.com/sandeepmistry/bleno)
 *
 * Features include:
 * - Positive response to any password
 * - Valid advertisement
 * - Valid scan response
 * - Valid response to "initial" data read of config
 *   file and current temperature/humidity
 *
 * TO DO:
 * - Implement response for a normal "readout"
 */

var util = require('util');
var bleno = require('bleno');
var sleep = require('sleep');

var name = 'MX1101';

// Define the Device ID service
var service_0c= new bleno.PrimaryService({
	uuid: '180a',
	characteristics:[
		new bleno.Characteristic({
			uuid: '2a29',
			properties: ['read'],
			secure: [],
			value: 'Onset Computer Corp',
		}),
		new bleno.Characteristic({
			uuid: '2a24',
			properties: ['read'],
			secure: [],
			value: 'MX1101',
		}),
		new bleno.Characteristic({
			uuid: '2a25',
			properties: ['read'],
			secure: [],
			value: '10912519',
		}),
		new bleno.Characteristic({
			uuid: '2a26',
			properties: ['read'],
			secure: [],
			value: '57',
		}),
		new bleno.Characteristic({
			uuid: '2a28',
			properties: ['read'],
			secure: [],
			value: '72'
		})
	]
});

// Define Onset's C2 Service
var service_17= new bleno.PrimaryService({
	uuid: '65E16E4F-ED4E-4641-AC49-83CCBCE6CBCF',
	characteristics:[
		new bleno.Characteristic({
			uuid: '65E16F4F-ED4E-4641-AC49-83CCBCE6CBCF', // Handle: 0x19
			properties: ['write','notify'],
			secure: [],
			value: null,
			onWriteRequest: function(data,offset,withoutResponse,callback){
				callback(this.RESULT_SUCCESS); // Write response
				respondHandle19(data,this.updateValueCallback); // Notify
			}
		}),
		new bleno.Characteristic({
			uuid: '65E16F50-ED4E-4641-AC49-83CCBCE6CBCF',
			properties: ['read', 'write'],
			secure: [],
			value: 4096,
		}),
		new bleno.Characteristic({
			uuid: '65E16F52-ED4E-4641-AC49-83CCBCE6CBCF',
			properties: ['write','notify'],
			secure: [],
			value: null,
		}),
		new bleno.Characteristic({
			uuid: '65E16F53-ED4E-4641-AC49-83CCBCE6CBCF',
			properties: ['read','write'],
			secure: [],
			value: 0,
			descriptors: []
		})
	]
});

// Define what happens when we receive a "write request" to the C2 handle
function respondHandle19(d,notify){
	var notifications = [];
	
	// Check command that came in... what is the app trying to do?
	d = d.toString('hex');
	// Authentication request
	if (d.indexOf('010104051c01') == 0) {
		console.log('Captured authentication request...');
		notifications = [
			'010102051c00051c000000000000000000000000'
		];

	// Initial information request
	} else if (d.indexOf('01010a0a010000000000000400') == 0) {
		console.log('Captured basic information request...');
		notifications = [
			'01370a0100484f424f880d0400001000881d0400',
			'0200014a886301008801020f1b88020224028803',
			'0302004888bd02003988041a4f6e73657420436f',
			'046d707574657220436f72706f726174696f6e88',
			'0505064d58313130318806083130393132353139',
			'0688b7010088b80100880708141007050e380c2c',
			'0788090400000001880a08313039313235313988',
			'083429484f424f6d6f62696c652d312e342e3120',
			'096275696c643a303230342d416e64726f69645f',
			'0a352e302e32880e0400000020880f081410040e',
			'0b0a351300881204ffffc7c08813010188141041',
			'0c6d65726963612f4e65775f596f726b881e0440',
			'0d3b8000881f040002000088b6074d7947726f75',
			'0e708892010088b10100885f010088bb02000188',
			'0fc10600001e0027608808040000025888160088',
			'108800880b0101880c0121881100881600888800',
			'11880b0101880c0124881100881600888800880b',
			'120100880c017f881100ffff0b0100880c017f88',
			'131100ffffffffffffffffff1100ffffffffffff',
			'14ffffffffffffffffffffffffffffffffffffff',
			'15ffffffffffffffffffffffffffffffffffffff',
			'16ffffffffffffffffffffffffffffffffffffff',
			'17ffffffffffffffffffffffffffffffffffffff',
			'18ffffffffffffffffffffffffffffffffffffff',
			'19ffffffffffffffffffffffffffffffffffffff',
			'1affffffffffffffffffffffffffffffffffffff',
			'1bffffffffffffffffffffffffffffffffffffff',
			'1cffffffffffffffffffffffffffffffffffffff',
			'1dffffffffffffffffffffffffffffffffffffff',
			'1effffffffffffffffffffffffffffffffffffff',
			'1fffffffffffffffffffffffffffffffffffffff',
			'20ffffffffffffffffffffffffffffffffffffff',
			'21ffffffffffffffffffffffffffffffffffffff',
			'22ffffffffffffffffffffffffffffffffffffff',
			'23ffffffffffffffffffffffffffffffffffffff',
			'24ffffffffffffffffffffffffffffffffffffff',
			'25ffffffffffffffffffffffffffffffffffffff',
			'26ffffffffffffffffffffffffffffffffffffff',
			'27ffffffffffffffffffffffffffffffffffffff',
			'28ffffffffffffffffffffffffffffffffffffff',
			'29ffffffffffffffffffffffffffffffffffffff',
			'2affffffffffffffffffffffffffffffffffffff',
			'2bffffffffffffffffffffffffffffffffffffff',
			'2cffffffffffffffffffffffffffffffffffffff',
			'2dffffffffffffffffffffffffffffffffffffff',
			'2effffffffffffffffffffffffffffffffffffff',
			'2fffffffffffffffffffffffffffffffffffffff',
			'30ffffffffffffffffffffffffffffffffffffff',
			'31ffffffffffffffffffffffffffffffffffffff',
			'32ffffffffffffffffffffffffffffffffffffff',
			'33ffffffffffffffffffffffffffffffffffffff',
			'34ffffffffffffffffffffffffffffffffffffff',
			'35ffffffffffffffffffffffffffffffffffffff',
			'36ffffffffffffffffffffffffffffffffffffff',
			'3702ffff00000000000000000000000000000000'
		];

	// Periodic request - probably request for current temp/humidity
	} else if (d.indexOf('0101080405000000000000') == 0) {
		notifications = [
			'01020405000405920000100a02580000b1000000',
			'0207000000001000030000000000000000000000'
		];
		
	// Periodic request - probably request for current temp/humidity
	} else if (d.indexOf('010102020c000000000000') == 0) {
		notifications = [
			'010108020c00020c000000000000000000000000'
		];
	
	// Periodic request - probably request for current temp/humidity
	} else if (d.indexOf('0101080404000000000000') == 0) {
		notifications = [
			'0102040400040400000828000025e70000077f9b',
			'0205120000000000000000000000000000000000'
		];

	// Request for firmware update
	} else if (d.indexOf('0101080203000000000000') == 0) {
		notifications = [
			'01010e0203000203400005080000000000000000'
		];

	// Request for firmware update
	} else if (d.indexOf('0101080108550000000000') == 0) {
		notifications = [
			'0101020108000000000000000000000000000000'
		];
	}

	console.log(d)

	// Send notifications based on the command we received
	notifications.forEach(function(value){
		notify(new Buffer(value,'hex'));
		sleep.usleep(50000);
	});
}

// Wait until the BLE radio powers on before attempting to advertise.
// If you don't have a BLE radio, then it will never power on!
bleno.on('stateChange', function(state) {
  if (state === 'poweredOn') {
	var myScanData = new Buffer('06084d5831313031','hex');
	var myAdvData = new Buffer('020106020a0015ffc500050783a60002240000000800d219082b2998','hex');
	bleno.startAdvertisingWithEIRData(myAdvData, myScanData, function(err) {
		if (err) {
			console.log(err);	
		}
	});
  }
  else {
    bleno.stopAdvertising();
  }
});

// Start services once we begin advertising
bleno.on('advertisingStart', function(err) {
  if (!err) {
    console.log('Advertising...');
    bleno.setServices([
 	service_0c,
     	service_17
    ]);
  }
});
