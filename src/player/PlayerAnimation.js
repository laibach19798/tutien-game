// Chỉ lo chọn frame + vẽ các layer (base, tóc, áo, vũ khí... cùng layout sheet).
(function(T){
T.PlayerAnimation=class{
  constructor(assets,layers){this.assets=assets;this.layers=layers;this.name='IDLE';this.dir='DOWN';this.t=0;this.frame=0;}
  play(name,dir){if(name!==this.name){this.name=name;this.t=0;}this.dir=dir;}
  update(dt){
    const clip=T.ANIMATIONS[this.name],d=T.DIRECTIONS[this.dir];
    const n=T.PLAYER_BASE_META.frames[clip.sheet][d.row];
    this.t+=dt;const f=Math.floor(this.t*T.CONFIG[clip.fpsKey]);this.frame=clip.loop===false?Math.min(f,n-1):f%n;
  }
  finished(){const clip=T.ANIMATIONS[this.name];return clip.loop===false&&this.t*T.CONFIG[clip.fpsKey]>=T.PLAYER_BASE_META.frames[clip.sheet][T.DIRECTIONS[this.dir].row];}
  draw(ctx,x,y){
    const clip=T.ANIMATIONS[this.name],F=clip.frame||T.CONFIG.FRAME,s=T.CONFIG.PLAYER_SPRITE_SCALE,d=T.DIRECTIONS[this.dir];
    for(const l of this.layers){
      const img=this.assets.get(l.path+'/'+clip.sheet);if(!img)continue; // layer không có sheet cho animation này (vd. kiếm lúc đi bộ)
      ctx.save();ctx.translate(x,y);ctx.scale(d.flip?-s:s,s);
      ctx.drawImage(img,this.frame*F.w,d.row*F.h,F.w,F.h,-F.ax,-F.ay,F.w,F.h);
      ctx.restore();
    }
  }
};
})(window.Tutien=window.Tutien||{});
