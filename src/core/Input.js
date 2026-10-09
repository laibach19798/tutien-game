(function(T){
const MAP={KeyW:'u',ArrowUp:'u',KeyS:'d',ArrowDown:'d',KeyA:'l',ArrowLeft:'l',KeyD:'r',ArrowRight:'r'};
T.Input=class{
  constructor(stick){
    this.stick=stick||null;this.down=new Set();this.shift=false;this.jumpQ=false;this.atkQ=false;
    addEventListener('keydown',e=>{
      if(MAP[e.code]){this.down.add(e.code);e.preventDefault();}
      if(e.code==='ShiftLeft'||e.code==='ShiftRight')this.shift=true;
      if(e.code==='KeyJ'&&!e.repeat)this.atkQ=true;
      if(e.code==='Space'){if(!e.repeat)this.jumpQ=true;e.preventDefault();}
    });
    addEventListener('keyup',e=>{this.down.delete(e.code);if(e.code==='ShiftLeft'||e.code==='ShiftRight')this.shift=false;});
    addEventListener('blur',()=>{this.down.clear();this.shift=false;});
  }
  pressAttack(){this.atkQ=true;}
  consumeAttack(){const j=this.atkQ;this.atkQ=false;return j;}
  pressJump(){this.jumpQ=true;}                       // nút ảo trên điện thoại gọi hàm này
  consumeJump(){const j=this.jumpQ;this.jumpQ=false;return j;}
  run(){return this.shift||(!!this.stick&&this.stick.magnitude()>=T.CONFIG.STICK_RUN_THRESHOLD);}
  has(d){for(const c of this.down)if(MAP[c]===d)return true;return false;}
  axis(){
    const x=(this.has('r')?1:0)-(this.has('l')?1:0),y=(this.has('d')?1:0)-(this.has('u')?1:0);
    if(x||y)return {x,y};
    return this.stick?this.stick.vector():{x:0,y:0};
  }
};
})(window.Tutien=window.Tutien||{});
