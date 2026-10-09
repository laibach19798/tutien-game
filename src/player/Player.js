(function(T){
T.Player=class{
  constructor(assets,x,y){
    this.x=x;this.y=y;this.facing='DOWN';this.jumping=false;this.jumpRun=false;this.attacking=false;
    this.equipped=Object.assign({},T.DEFAULT_EQUIP);
    this.movement=new T.PlayerMovement();
    this.anim=new T.PlayerAnimation(assets,this.buildLayers());
  }
  buildLayers(){
    const L=[{id:'base',path:'player/base'}];
    for(const slot of T.EQUIP_SLOTS){const id=this.equipped[slot];if(id)L.push({id,path:T.ITEMS[id].path});}
    return L;
  }
  equip(slot,id){this.equipped[slot]=id||null;this.anim.layers=this.buildLayers();}
  // đổi sang món kế tiếp trong slot (cuối danh sách -> tháo ra); trả về id đang mặc
  cycle(slot){const ids=Object.keys(T.ITEMS).filter(k=>T.ITEMS[k].slot===slot),i=ids.indexOf(this.equipped[slot]);this.equip(slot,i+1<ids.length?ids[i+1]:null);return this.equipped[slot];}
  toggle(slot){this.equip(slot,this.equipped[slot]?null:T.DEFAULT_EQUIP[slot]);return !!this.equipped[slot];}
  update(dt,input,world){
    const C=T.CONFIG,run=input.run(),wantJump=input.consumeJump(),wantAtk=input.consumeAttack();
    if(wantAtk&&!this.attacking&&!this.jumping){this.attacking=true;this.anim.play('ATTACK',this.facing);this.anim.t=0;}
    if(this.attacking){ // chém: đứng yên, khoá hướng, chạy hết animation rồi về bình thường
      this.anim.play('ATTACK',this.facing);this.anim.update(dt);
      if(this.anim.finished())this.attacking=false;
      return;
    }
    if(wantJump&&!this.jumping){this.jumping=true;this.jumpRun=run;this.anim.play('JUMP',this.facing);this.anim.t=0;}
    if(this.jumping){ // nhảy: khoá hướng nhìn, vẫn di chuyển được với tốc độ lúc bắt đầu nhảy
      this.movement.update(this,dt,input.axis(),world,this.jumpRun?C.PLAYER_RUN_SPEED_MULT:1);
      this.anim.play('JUMP',this.facing);this.anim.update(dt);
      if(this.anim.finished())this.jumping=false;
      return;
    }
    const m=this.movement.update(this,dt,input.axis(),world,run?C.PLAYER_RUN_SPEED_MULT:1);
    if(m.moving)this.facing=T.dirFromVector(m.dx,m.dy);
    this.anim.play(m.moving?(run?'RUN':'WALK'):'IDLE',this.facing);
    this.anim.update(dt);
  }
  draw(ctx){this.anim.draw(ctx,Math.round(this.x),Math.round(this.y));}
};
})(window.Tutien=window.Tutien||{});
