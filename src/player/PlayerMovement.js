// Chỉ lo vị trí/vận tốc. Không biết gì về animation.
(function(T){
T.PlayerMovement=class{
  update(p,dt,axis,world,speedMult=1){
    const len=Math.hypot(axis.x,axis.y);
    if(!len)return {moving:false,dx:0,dy:0};
    const s=T.CONFIG.PLAYER_MOVE_SPEED*speedMult/len; // normalize: đi chéo = đi thẳng
    const b=world.bounds;
    p.x=Math.min(Math.max(p.x+axis.x*s*dt,b.minX),b.maxX);
    p.y=Math.min(Math.max(p.y+axis.y*s*dt,b.minY),b.maxY);
    return {moving:true,dx:axis.x,dy:axis.y};
  }
};
})(window.Tutien=window.Tutien||{});
