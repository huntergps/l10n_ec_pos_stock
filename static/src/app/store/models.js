/** @odoo-module */
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

patch(PosStore.prototype, {
    async processServerData(loadedData) {
        await super.processServerData(...arguments);
        this.custom_stock_locations = this.data.models["stock.location"].filter(location =>
            location === this.config.stock_location_id
        );
    },

    async addLineToCurrentOrder(vals, opts = {}, configure = true) {
        let self = this;
        let pos_config = self.config;
        const product = vals.product_id;
        let allow_order = pos_config.pos_allow_order;
        let deny_order= pos_config.pos_deny_order || 0;
        let call_super = true;

        if(pos_config.pos_display_stock && product.type == 'consu' && product.is_storable){
            if (allow_order == false){
                if (pos_config.pos_stock_type == 'onhand'){
                    if ( product.bi_on_hand <= 0 ){
                        call_super = false;
                        self.dialog.add(AlertDialog, {
                            title: _t('Venta Negada'),
                            body: _t("Producto agotado:\n" + product.display_name),
                        });
                    }
                }
                if (pos_config.pos_stock_type == 'available'){
                    if ( product.bi_available <= 0 ){
                        call_super = false;
                        self.dialog.add(AlertDialog, {
                            title: _t('Venta Negada'),
                            body: _t("Producto agotado:\n" + product.display_name),
                        });
                    }
                }
            }else{
                if (pos_config.pos_stock_type == 'onhand'){
                    if ( product.bi_on_hand <= deny_order ){
                        call_super = false;
                        self.dialog.add(AlertDialog, {
                            title: _t('Venta Negada'),
                            body: _t("Producto agotado:\n" + product.display_name),
                        });
                    }
                }
                if (pos_config.pos_stock_type == 'available'){
                    if ( product.bi_available <= deny_order ){
                        call_super = false;
                        self.dialog.add(AlertDialog, {
                            title: _t('Venta Negada'),
                            body: _t("Producto agotado:\n" + product.display_name),
                        });
                    }
                }
            }
        }
        if(call_super){
            super.addLineToCurrentOrder(vals, opts = {}, configure = true);
        }
    },

    product_total(){
        let order = this.pos.get_order();
        var orderlines = order.get_orderlines();
        return orderlines.length;
    },

    set_interval(interval){
        this.interval=interval;
    },

    async pay() {
        var self = this;
        let order = this.get_order();
        let lines = order.get_orderlines();
        let pos_config = self.config;
        let allow_order = pos_config.pos_allow_order;
        let deny_order = pos_config.pos_deny_order || 0;
        let call_super = true;

        if (pos_config.pos_display_stock) {
            let prod_used_qty = {};
            lines.forEach(line => {
                let prd = line.product_id;
                if (prd.type == 'consu' && prd.is_storable) {
                    if (pos_config.pos_stock_type == 'onhand') {
                        if (prd.id in prod_used_qty) {
                            let old_qty = prod_used_qty[prd.id][1];
                            prod_used_qty[prd.id] = [prd.bi_on_hand, line.qty + old_qty];
                        } else {
                            prod_used_qty[prd.id] = [prd.bi_on_hand, line.qty];
                        }
                    }
                    if (pos_config.pos_stock_type == 'available') {
                        if (prd.id in prod_used_qty) {
                            let old_qty = prod_used_qty[prd.id][1];
                            prod_used_qty[prd.id] = [prd.bi_available, line.qty + old_qty];
                        } else {
                            prod_used_qty[prd.id] = [prd.bi_available, line.qty];
                        }
                    }
                }
            });

            for (let [i, pq] of Object.entries(prod_used_qty)) {
                let product = self.models['product.product'].getBy('id',i)
                if (allow_order == false && pq[0] < pq[1]) {
                    call_super = false;
                    self.dialog.add(AlertDialog, {
                        title: _t('Venta Negada'),
                        body: _t("Producto agotado: " + product.display_name),
                    });
                }
                let check = pq[0] - pq[1];
                if (allow_order == true && check < deny_order) {
                    call_super = false;
                    self.dialog.add(AlertDialog, {
                        title: _t('Venta Negada'),
                        body: _t("Producto agotado: " + product.display_name),
                    });
                }
            }
        }
        if (call_super) {
            super.pay();
        }
    }

});
