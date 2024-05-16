const { randomInt, createHash } = require('crypto');
const readline = require('readline').createInterface({
  input: process.stdin,
  output: process.stdout,
});


const prefix_len = 192;
const alphabet = 'abcdefghijklmnopqrstuvwxyz';
let output = '';
for (let i = 0; i < prefix_len+128; i++) {
    output += alphabet[Math.floor(Math.random() * alphabet.length)];
}

const prefix = output.substring(0, prefix_len);
const expected = output.substring(prefix_len);

console.log(prefix);
console.log(createHash('sha256').update(expected, 'utf8').digest('hex'));

readline.question('❓️\n', guess => {
    readline.close();
    if (guess === expected) {
        console.log('✅');
        process.exit(42);
    } else {
        console.log('❌');
        process.exit(1);
    }
});

