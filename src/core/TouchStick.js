// Joystick ảo cho điện thoại. Trả về vector hướng (độ dài 1) hoặc 0 khi thả tay.
(function(T){
T.TouchStick=class{
  constructor(zone,knob){
    this.zone=zone;this.knob=knob;this.id=null;this.x=0;this.y=0;this.R=56;this.deadzone=0.25;
    const set=e=>{
      const r=zone.getBoundingClientRect(),cx=r.left+r.width/2,cy=r.top+r.height/2;
      let dx=e.clientX-cx,dy=e.clientY-cy;const m=Math.hypot(dx,dy),k=m>this.R?this.R/m:1;
      dx*=k;dy*=k;this.x=dx/this.R;this.y=dy/this.R;knob.style.transform='translate('+dx+'px,'+dy+'px)';
    };
    zone.addEventListener('pointerdown',e=>{if(this.id!==null)return;this.id=e.pointerId;try{zone.setPointerCapture(e.pointerId);}catch(_){}set(e);e.preventDefault();});
    zone.addEventListener('pointermove',e=>{if(e.pointerId===this.id)set(e);});
    const end=e=>{if(e.pointerId!==this.id)return;this.id=null;this.x=this.y=0;knob.style.transform='translate(0px,0px)';};
    zone.addEventListener('pointerup',end);zone.addEventListener('pointercancel',end);
  }
  magnitude(){return Math.min(1,Math.hypot(this.x,this.y));}
  vector(){const m=Math.hypot(this.x,this.y);return m<this.deadzone?{x:0,y:0}:{x:this.x/m,y:this.y/m};}
};
})(window.Tutien=window.Tutien||{});
