var camera, scene, renderer, stats, material;
var mouseX = 0, mouseY = 0;

var windowHalfX = window.innerWidth / 2;
var windowHalfY = window.innerHeight / 2;

// Draw the systems
function draw_stars() {
    systems = json_map['render_stars']['systems'];

    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 2, 2000 );
    camera.position.z = 100;

    scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2( 0x000000, 0.001 );

    var geometry = new THREE.BufferGeometry();
    var positions = [];
    var sizes = [];
    var colors = [];

    var sprite = new THREE.TextureLoader().load( '/particle.png' );

    for(var i=0; i<systems.length; i++) {
        positions.push(systems[i].x, systems[i].y, systems[i].z);
        sizes.push(systems[i].size + 200);
        var color = new THREE.Color(systems[i].color);
        colors.push(color.r, color.g, color.b, 1.0);
        console.log(systems[i].name, systems[i].color, color.r, color.g, color.b);
    }

    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    geometry.setAttribute('size', new THREE.Float32BufferAttribute(sizes, 1));
    geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 4));

    material = new THREE.ShaderMaterial({
		vertexShader: document.getElementById('vertexshader').textContent,
		fragmentShader: document.getElementById('fragmentshader').textContent,
        transparent: true
    });
//    material = new THREE.ShaderMaterial( {
//            size: 35,
//            sizeAttenuation: false,
//            map: sprite,
//	        uniforms: {
//				color: { value: new THREE.Color( 0xffffff ) },
//				pointTexture: { value: new THREE.TextureLoader().load( "/particle.png" ) }
//			},
//			vertexShader: document.getElementById( 'vertexshader' ).textContent,
//			fragmentShader: document.getElementById( 'fragmentshader' ).textContent,
//			alphaTest: 0.9
//		} );
//    material = new THREE.PointsMaterial( { size: 35, sizeAttenuation: false, map: sprite, alphaTest: 0.5, transparent: true } );
//    material.color.setHSL( 1.0, 0.3, 0.7 );

    var points = new THREE.Points(geometry, material);
    scene.add(points);

    //

    renderer = new THREE.WebGLRenderer();
    renderer.setPixelRatio( window.devicePixelRatio );
    renderer.setSize( window.innerWidth, window.innerHeight );
    document.getElementById('play_mode').appendChild( renderer.domElement );

    //

//    document.addEventListener( 'mousemove', onDocumentMouseMove, false );
    document.addEventListener( 'touchstart', onDocumentTouchStart, false );
    document.addEventListener( 'touchmove', onDocumentTouchMove, false );

    //

    window.addEventListener( 'resize', onWindowResize, false );

    animate();
}

function onWindowResize() {

    windowHalfX = window.innerWidth / 2;
    windowHalfY = window.innerHeight / 2;

    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();

    renderer.setSize( window.innerWidth, window.innerHeight );

}

function onDocumentMouseMove( event ) {

    mouseX = event.clientX - windowHalfX;
    mouseY = event.clientY - windowHalfY;

}

function onDocumentTouchStart( event ) {

    if ( event.touches.length == 1 ) {

        event.preventDefault();

        mouseX = event.touches[ 0 ].pageX - windowHalfX;
        mouseY = event.touches[ 0 ].pageY - windowHalfY;

    }

}

function onDocumentTouchMove( event ) {

    if ( event.touches.length == 1 ) {

        event.preventDefault();

        mouseX = event.touches[ 0 ].pageX - windowHalfX;
        mouseY = event.touches[ 0 ].pageY - windowHalfY;

    }

}

function animate() {

    requestAnimationFrame( animate );

    render();
}

function render() {

    var time = Date.now() * 0.00005;

    camera.position.x += ( mouseX - camera.position.x ) * 0.05;
    camera.position.y += ( - mouseY - camera.position.y ) * 0.05;

    camera.lookAt( scene.position );

    var h = ( 360 * ( 1.0 + time ) % 360 ) / 360;
//    material.color.setHSL( h, 0.5, 0.5 );

    renderer.render( scene, camera );

}
