"use client";
import { ProductProps } from "@/lib/types";
import { useQuery } from "@tanstack/react-query";
import { fetchData } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { format } from "date-fns";

interface ProductQuantity {
  product: ProductProps;
  quantity: number;
}

interface Purchase {
  id: number;
  products: ProductQuantity[];
  total_price: number;
  created_at: string;
}

export default function Home() {

  const { data: purchases, isLoading: isLoading, isError: isError } = useQuery({
    queryKey: ["history"],
    queryFn: fetchPurchases
  });

  if (isLoading || !purchases) {
    return (
      <div>loading...</div>

    );
  }
  if (isError) {
    return <div>error</div>;
  }


  return (
    <div className={"flex flex-col justify-center items-center mt-4 space-y-6"}>
      {purchases.length === 0 ? (
        <p>Historia jest pusta</p>
      ) : (
        purchases.map((purchase: Purchase) => (
          <Card key={purchase.id} className="w-[650px]">
            <CardHeader>
              <CardTitle>Total: {purchase.total_price}zł</CardTitle>
              <CardDescription>{format(new Date(purchase.created_at), "d/MM/y")}</CardDescription>
            </CardHeader>
            {purchase.products.map((item: ProductQuantity) => (
                <Card key={item.product.id} className="w-[600px]">
                  <CardHeader>
                    <CardTitle>{item.product.name}, {item.product.price} zł</CardTitle>
                    <CardDescription>{item.product.description}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className={"flex flex-col justify-center align-items-center"}>
                      <div className={"space-x-4 flex"}>
                        <Button disabled={true}>{item.quantity}</Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )
            )}
          </Card>
        ))
      )

      }
    </div>
  );
}

const fetchPurchases = async () => fetchData<Purchase[]>("purchases/");