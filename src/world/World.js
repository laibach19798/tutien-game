// Map = 1 ảnh nền vẽ sẵn, phóng to số nguyên (MAP_SCALE) để khớp tỉ lệ nhân vật.
// Sau này thêm: lớp collision, lớp che (cây/mái nhà đè lên nhân vật), nhiều map.
(function(T){
T.World=class{
  constructor(assets){
    const C=T.CONFIG;this.img=assets.get('world/village');this.s=C.MAP_SCALE;
    this.w=this.img.width*this.s;this.h=this.img.height*this.s;
    this.bounds={minX:40,minY:60,maxX:this.w-40,maxY:this.h-20};
    this.spawn={x:C.MAP_SPAWN.x*this.s,y:C.MAP_SPAWN.y*this.s};
  }
  drawGround(ctx,r){
    const s=this.s,sx=Math.max(0,Math.floor(r.x/s)),sy=Math.max(0,Math.floor(r.y/s)),
      sw=Math.min(this.img.width-sx,Math.ceil(r.w/s)+2),sh=Math.min(this.img.height-sy,Math.ceil(r.h/s)+2);
    if(sw>0&&sh>0)ctx.drawImage(this.img,sx,sy,sw,sh,sx*s,sy*s,sw*s,sh*s);
  }
  visibleProps(r){return [];} // chỗ để vật thể y-sort (cây, nhà) khi có
};
})(window.Tutien=window.Tutien||{});
