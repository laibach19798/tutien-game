// Mọi đường dẫn asset nằm ở đây (cần equipment.js nạp trước). Mỗi layer = 1 thư mục chứa các sheet cùng bố cục.
(function(T){
const ANIMS=['idle','walk','run','jump','attack'];
const L=(path,anims)=>Object.fromEntries(anims.map(a=>[path+'/'+a,'assets/'+path+'/'+a+'.png']));
const items=Object.values(T.ITEMS).reduce((o,it)=>Object.assign(o,L(it.path,it.anims||ANIMS)),{});
T.ASSET_MANIFEST=Object.assign({},L('player/base',ANIMS),items,{'world/village':'assets/world/village.png'});
})(window.Tutien=window.Tutien||{});
