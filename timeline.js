/**
 * @author dbm
 */
var doc = new GLGE.Document();
doc.onLoad = function(){
    //create the renderer
    var canvas = document.getElementById('canvas');

    var world_z = 0;
    var glgedoc = this;
    canvas.onmousewheel = function( e ){
        world_z += e.wheelDelta * 0.0025;
        glgedoc.getElement("world").setLocZ(world_z)
//        glgedoc.getElement("worldmap").setReflectivity(0)
//        glgedoc.getElement("worldmap").setBinaryAlpha(true)
//        glgedoc.getElement("worldmap").setAlpha(0.3)
//        glgedoc.getElement("worldmap_ml").setAlpha(0.2)
//        glgedoc.getElement("worldmap").setShadeless(false)
//        console.log("WHEEL ev:", e.wheelDelta, glgedoc.getElement("world"));
        return false;
    }
    
    var gameRenderer = new GLGE.Renderer(canvas);
    gameScene = new GLGE.Scene();
    gameScene = doc.getElement("mainscene");
    gameRenderer.setScene(gameScene);
    
    var mouse = new GLGE.MouseInput(canvas);
    var keys = new GLGE.KeyInput();
    var mouseovercanvas;
    var hoverobj;
    var mouseLastX = parseInt(document.getElementById("container").style.width.replace("px", "")) / 2;
    function mouselook(){
        if (mouseovercanvas) {
            var mousepos = mouse.getMousePosition();
            mousepos.x = mousepos.x - document.getElementById("container").offsetLeft;
            mousepos.y = mousepos.y - document.getElementById("container").offsetTop;
            var camera = gameScene.camera;
            camerarot = camera.getRotation();
            inc = (mousepos.y - (canvas.offsetHeight / 2)) / 500;
            //      var trans=camera.getRotMatrix().x([0,0,-1,1]);
            var trans = GLGE.mulMat4Vec4(camera.getRotMatrix(), [0, 0, -1, 1]);
            var mag = Math.pow(Math.pow(trans[0], 2) + Math.pow(trans[1], 2), 0.5);
            trans[0] = trans[0] / mag;
            trans[1] = trans[1] / mag;
            camera.setRotX(1.56 - trans[1] * inc);
            camera.setRotZ(-trans[0] * inc);
            var width = canvas.offsetWidth;
            if (mousepos.x < width * 0.225) {
                var turn = Math.pow((mousepos.x - width * 0.25) / (width * 0.25), 2) * 0.005 * (now - lasttime);
                camera.setRotY(camerarot.y + turn);
            }
            else {
                if (mousepos.x > width * 0.775) {
                    var turn = Math.pow((mousepos.x - width * 0.75) / (width * 0.25), 2) * 0.005 * (now - lasttime);
                    camera.setRotY(camerarot.y - turn);
                }
                else {
                    camera.setRotY(camerarot.y + (mouseLastX - mousepos.x) * 0.001)
                }
            }
            mouseLastX = mousepos.x
        }
    }
    
    function checkkeys(){
        var camera = gameScene.camera;
        camerapos = camera.getPosition();
        camerarot = camera.getRotation();
        var mat = camera.getRotMatrix();
        //  var trans=mat.x([0,0,-1]);
        var trans = GLGE.mulMat4Vec4(mat, [0, 0, -1, 1]);
        var mag = Math.pow(Math.pow(trans[0], 2) + Math.pow(trans[1], 2), 0.5);
        trans[0] = trans[0] / mag;
        trans[1] = trans[1] / mag;
        var yinc = 0;
        var xinc = 0;
        var zinc = 0;
        if (keys.isKeyPressed(GLGE.KI_M)) {
            addduck();
        }
        if (keys.isKeyPressed(GLGE.KI_W)) {
            yinc = yinc + parseFloat(trans[1]);
            xinc = xinc + parseFloat(trans[0]);
        }
        if (keys.isKeyPressed(GLGE.KI_S)) {
            yinc = yinc - parseFloat(trans[1]);
            xinc = xinc - parseFloat(trans[0]);
        }
        if (keys.isKeyPressed(GLGE.KI_A)) {
            yinc = yinc + parseFloat(trans[0]);
            xinc = xinc - parseFloat(trans[1]);
        }
        if (keys.isKeyPressed(GLGE.KI_D)) {
            yinc = yinc - parseFloat(trans[0]);
            xinc = xinc + parseFloat(trans[1]);
        }
        
        if (keys.isKeyPressed(GLGE.KI_R)) {
            zinc += 0.6;
        }
        
        if (keys.isKeyPressed(GLGE.KI_F)) {
            zinc -= 0.6;
        }
        
        if (xinc != 0 || yinc != 0 || zinc != 0) {
            camera.setLocY(camerapos.y + yinc * 0.01 * (now - lasttime));
            camera.setLocX(camerapos.x + xinc * 0.01 * (now - lasttime));
            camera.setLocZ(camerapos.z + zinc * 0.01 * (now - lasttime))
        }
    }
    
    var lasttime = 0;
    var frameratebuffer = 60;
    start = parseInt(new Date().getTime());
    var now;
    function render(){
        now = parseInt(new Date().getTime());
        frameratebuffer = Math.round(((frameratebuffer * 9) + 1000 / (now - lasttime)) / 10);
        mouselook();
        checkkeys();
        gameRenderer.render();
        lasttime = now;
    }
    setInterval(render, 1);
    var inc = 0.2;
    document.getElementById("canvas").onmouseover = function(e){
        mouseovercanvas = true;
    }
    document.getElementById("canvas").onmouseout = function(e){
        mouseovercanvas = false;
    }
}
doc.load("level.xml");
