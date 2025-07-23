let scene, camera, renderer, carMeshes = [];

document.getElementById("control-form").addEventListener("submit", async function (e) {
    e.preventDefault();
    const numCars = document.getElementById("numCars").value;
    const start = document.getElementById("start").value.split(',').map(Number);
    const end = document.getElementById("end").value.split(',').map(Number);
    const weather = document.getElementById("weather").value;

    await fetch("/start_simulation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ num_cars: numCars, start_point: start, end_point: end, weather: weather })
    });

    initThreeJS();
    animate();
});

function initThreeJS() {
    carMeshes = [];

    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / 600, 0.1, 1000);
    camera.position.set(0, -100, 100);
    camera.lookAt(0, 0, 0);

    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, 600);
    document.getElementById("container").innerHTML = '';
    document.getElementById("container").appendChild(renderer.domElement);
}

async function animate() {
    requestAnimationFrame(animate);

    const res = await fetch("/get_positions");
    const data = await res.json();

    while (scene.children.length) {
        scene.remove(scene.children[0]);
    }

    data.forEach(pos => {
        const car = new THREE.Mesh(new THREE.SphereGeometry(1.5), new THREE.MeshBasicMaterial({ color: 0x00aaff }));
        car.position.set(pos[0], pos[1], pos[2]);
        scene.add(car);
    });

    renderer.render(scene, camera);
}
