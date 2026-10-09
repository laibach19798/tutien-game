(function(T){
T.Camera=class{
  constructor(){this.x=0;this.y=0;this.zoom=1;this.offsetX=0;this.offsetY=0; // offset/zoom: chỗ gắn shake, boss cam, skill FX
    this.vw=0;this.vh=0;this.target=null;this.bounds=null;}
  resize(w,h){this.vw=w;this.vh=h;}
  follow(t,bounds){this.target=t;this.bounds=bounds;this.update(1e9);}
  update(dt){
    if(!this.target)return;
    const k=1-Math.exp(-T.CONFIG.CAMERA_FOLLOW_SPEED*dt);
    this.x+=(this.target.x-this.x)*k;
    this.y+=(this.target.y+T.CONFIG.CAMERA_TARGET_OFFSET_Y-this.y)*k;
    if(this.bounds){const hw=this.vw/2/this.zoom,hh=this.vh/2/this.zoom;
      this.x=this.bounds.w<hw*2?this.bounds.w/2:Math.min(Math.max(this.x,hw),this.bounds.w-hw);
      this.y=this.bounds.h<hh*2?this.bounds.h/2:Math.min(Math.max(this.y,hh),this.bounds.h-hh);}
  }
  rect(){const w=this.vw/this.zoom,h=this.vh/this.zoom;return {x:this.x+this.offsetX-w/2,y:this.y+this.offsetY-h/2,w,h};}
  begin(ctx){
    ctx.setTransform(this.zoom,0,0,this.zoom,Math.round(this.vw/2-(this.x+this.offsetX)*this.zoom),Math.round(this.vh/2-(this.y+this.offsetY)*this.zoom));
    ctx.imageSmoothingEnabled=false;
  }
  end(ctx){ctx.setTransform(1,0,0,1,0,0);}
};
})(window.Tutien=window.Tutien||{});
