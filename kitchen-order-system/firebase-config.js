// firebase-config.js
// Your Firebase configuration (converted to compat version)

const firebaseConfig = {
    apiKey: "AIzaSyB7xF2kP5jgH6xyGg7-S-T_QgMoBDIoBBc",
    authDomain: "kitchenordersystem-66eb2.firebaseapp.com",
    projectId: "kitchenordersystem-66eb2",
    storageBucket: "kitchenordersystem-66eb2.firebasestorage.app",
    messagingSenderId: "786074432195",
    appId: "1:786074432195:web:8381f2cba8f43002232876"
};

// Initialize Firebase (compat version - works with our SDKs)
firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();
