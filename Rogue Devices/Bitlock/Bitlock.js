var bleno = require('bleno');
var util = require('util');

var name = '00000d26';
var nonce = new Buffer ('00000000000000000000000000000104', 'hex')

var serviceUuids = ['693dfedf28344dbb8f59e426c093ba26'];
var Characteristic = bleno.Characteristic;
var Descriptor = bleno.Descriptor;
var PrimaryService = bleno.PrimaryService;

/* var a001516 = function() {
    a001516.super_.call(this, {
        uuid : '2a00',
        properties : ['read'],
        value: new Buffer([0x42, 0x69, 0x74, 0x6c, 0x6f, 0x63, 0x6b]),
	 });
};
util.inherits(a001516, Characteristic);     

a001516.prototype.onReadRequest = function(offset, callback) {
  console.log('EchoCharacteristic - onReadRequest: value = ' + this._value.toString('hex'));
  callback(this.RESULT_SUCCESS, this._value);
};

var a001718 = function() {
    a001718.super_.call(this, {
        uuid : '2a01',
        properties : ['read'],
        value: hex2a('0002'),
    });
};

util.inherits(a001718, Characteristic);     

a001718.prototype.onReadRequest = function(offset, callback) {
  console.log('EchoCharacteristic - onReadRequest: value = ' + this._value.toString('hex'));
  callback(this.RESULT_SUCCESS, this._value);
};

// // Attribute 1
function Services1() {
  Services1.super_.call(this, {
    uuid: '1800',
    characteristics: [
		new a001516(),
		new a001718(),
      ]
  });
}
util.inherits(Services1, PrimaryService); */ 

var a00293a = function() {
    a00293a.super_.call(this, {
        uuid : '0ebfc6e79cc54cbdaf21fee21256d4f9',
        properties : ['read', 'notify', 'indicate'],
        value: null,
    });
	this._value = new Buffer(hex2a('00000000000000000000000000000000'));
	this._updateValueCallback = null;

};
util.inherits(a00293a, Characteristic);     

a00293a.prototype.onReadRequest = function(offset, callback) {
  console.log('EchoCharacteristic - onReadRequest: value = ' + this._value.toString('hex'));
  callback(this.RESULT_SUCCESS, this._value);
};

a00293a.prototype.onSubscribe = function(maxValueSize, updateValueCallback) {
   //console.log('Indicate: ' + data.toString('hex'));
   this._value = nonce
   updateValueCallback(this._value);
   this._updateValueCallback = updateValueCallback;
}

a00293a.prototype.onUnsubscribe = function () {
    this._updateValueCallback = null;
}

/* a00293a.prototype.onNotify = function() {
   //console.log('Indicate: ' + data.toString('hex'));
   //var data1 = new Buffer(hex2a('0000000000000000000000000000001b'))
   //this.updateValueCallback(data1)
   //updateValueCallback(this._data1);
   this._value = hex2a('0000000000000000000000000000001b')
   this._updateValueCallback = updateValueCallback;
} */

var a002c2d = function() {
    a002c2d.super_.call(this, {
        uuid : 'b5db1ee05c2d4b56866d6297702f85d0',
        properties : ['read', 'writeWithoutResponse'],
        value: hex2a('00'),
    });
};
util.inherits(a002c2d, Characteristic);     

a002c2d.prototype.onReadRequest = function(offset, callback) {
  console.log('EchoCharacteristic - onReadRequest: value = ' + this._value.toString('hex'));
  callback(this.RESULT_SUCCESS, this._value);
};

a002c2d.prototype.onWriteRequest = function(data, offset, withoutResponse, callback) {
   console.log('WriteOnlyCharacteristic write request: ' + data.toString('hex') + ' ' + offset + ' ' + withoutResponse);
   callback(this.RESULT_SUCCESS)
};

var a003031 = function() {
    a003031.super_.call(this, {
        uuid : '618696477b4e46439c7695d745ce501e',
        properties : ['read', 'notify', 'indicate'],
        value: hex2a('00'),
    });
};
util.inherits(a003031, Characteristic);     

a003031.prototype.onReadRequest = function(offset, callback) {
  console.log('EchoCharacteristic - onReadRequest: value = ' + this._value.toString('hex'));
  callback(this.RESULT_SUCCESS, this._value);
};

var a003637 = function() {
    a003637.super_.call(this, {
        uuid : 'dc186f7438d347ecaf06521471d29fe0',
        properties : ['read', 'notify', 'indicate'],
        value: hex2a('00000000000000000000000000000000'),
    });
};

util.inherits(a003637, Characteristic);     

a003637.prototype.onReadRequest = function(offset, callback) {
  console.log('EchoCharacteristic - onReadRequest: value = ' + this._value.toString('hex'));
  callback(this.RESULT_SUCCESS, this._value);
};

// // Attribute 2
function Services2() {
  Services2.super_.call(this, {
    uuid: '693dfedf28344dbb8f59e426c093ba26',
    characteristics: [
		new a00293a(),
		new a002c2d(),
		new a003031(),
		new a003637(),
      ]
  });
}
util.inherits(Services2, PrimaryService); 

var a004e4f = function() {
    a004e4f.super_.call(this, {
        uuid : '2a29',
        properties : ['read'],
        value: hex2a('4d6573684d6f74696f6e'),
    });
};
util.inherits(a004e4f, Characteristic);     

a004e4f.prototype.onReadRequest = function(offset, callback) {
  console.log('EchoCharacteristic - onReadRequest: value = ' + this._value.toString('hex'));
  callback(this.RESULT_SUCCESS, this._value);
};

var a005051 = function() {
    a005051.super_.call(this, {
        uuid : '2a24',
        properties : ['read'],
        value: hex2a('30302e3035'),
    });
	this._value = new Buffer(0);
};

util.inherits(a005051, Characteristic);     

a005051.prototype.onReadRequest = function(offset, callback) {
  console.log('EchoCharacteristic - onReadRequest: value = ' + this._value.toString('hex'));
  
  callback(this.RESULT_SUCCESS, this._value);
};

var a005253 = function() {
    a005253.super_.call(this, {
        uuid : '2a23',
        properties : ['read'],
        value: hex2a('3030303030643236'),
    });
};

util.inherits(a005253, Characteristic);     

a005253.prototype.onReadRequest = function(offset, callback) {
  console.log('EchoCharacteristic - onReadRequest: value = ' + this._value.toString('hex'));
  callback(this.RESULT_SUCCESS, this._value);
};

// // Attribute 3
function Services3() {
  Services3.super_.call(this, {
    uuid: '180a',
    characteristics: [
		new a004e4f(),
		new a005051(),
		new a005253()
      ]
  });
}
util.inherits(Services3, PrimaryService); 

var a006063 = function() {
    a006063.super_.call(this, {
        uuid : '2a19',
        properties : ['read'],
        value: hex2a('64'),
    });
};

util.inherits(a006063, Characteristic);     

a006063.prototype.onReadRequest = function(offset, callback) {
  console.log('EchoCharacteristic - onReadRequest: value = ' + this._value.toString('hex'));
  callback(this.RESULT_SUCCESS, this._value);
};

// // Attribute 4
function Services4() {
  Services4.super_.call(this, {
    uuid: '180f',
    characteristics: [
		new a006063(),

      ]
  });
}
util.inherits(Services4, PrimaryService); 

var a007172 = function() {
    a007172.super_.call(this, {
        uuid : 'a58066e98f3e40a9b3cbd93240dbc2dc',
        properties : ['write', 'withoutResponse'],
        value: null,
    });
};
util.inherits(a007172, Characteristic);     

a007172.prototype.onWriteRequest = function(data, offset, withoutResponse, callback) {
   console.log('WriteOnlyCharacteristic write request: ' + data.toString('hex') + ' ' + offset + ' ' + withoutResponse);
   callback(this.RESULT_SUCCESS)
};

var a007374 = function() {
    a007374.super_.call(this, {
        uuid : '6dccad17fc5f43fb9b48c8de5c6a2b54',
        properties : ['read', 'notify'],
        value: hex2a('0000000000000000000000000000000000000000'),
    });
};

util.inherits(a007374, Characteristic);     

a007374.prototype.onReadRequest = function(offset, callback) {
  console.log('EchoCharacteristic - onReadRequest: value = ' + this._value.toString('hex'));
  callback(this.RESULT_SUCCESS, this._value);
};

// // Attribute 5
function Services5() {
  Services5.super_.call(this, {
    uuid: '96795a0efbc542198439a6bec823531b',
    characteristics: [
		new a007172(),
		new a007374(),
      ]
  });
}
util.inherits(Services5, PrimaryService);

bleno.on('stateChange', function(state) {
  console.log('on -> stateChange: ' + state);

  if (state === 'poweredOn') {
    bleno.startAdvertising(name, serviceUuids);
  } else {
    bleno.stopAdvertising();
  }
});

bleno.on('advertisingStart', function(error) {
  console.log('on -> advertisingStart: ' + (error ? 'error ' + error : 'success'));

  if (!error) {
        bleno.setServices([
          //new Services1(),
          new Services2(),
          new Services3(),
          new Services4(),
          new Services5(),

    ]);
  }
});

bleno.on('advertisingStop', function() {
  console.log('on -> advertisingStop');
});

bleno.on('servicesSet', function() {
  console.log('on -> servicesSet');
});

function hex2a(hex)
{
  var str = '';
  for (var i = 0; i < hex.length; i += 2)
    str += String.fromCharCode(parseInt(hex.substr(i,2), 16));
  return str;
}
