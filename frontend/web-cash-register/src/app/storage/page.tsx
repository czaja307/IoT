"use client";
import { useQuery } from "@tanstack/react-query";
import { fetchData } from "@/lib/api";
import { Card, CardHeader, CardTitle } from "@/components/ui/card";


export default function Home() {

  const { data: products, isLoading: isLoadingProducts, isError: isErrorProducts } = useQuery({
    queryKey: ["products"],
    queryFn: fetchProductsCount
  });

  console.log(products);


  if (isLoadingProducts || !products) {
    return (
      <div>loading...</div>

    );
  }
  if (isErrorProducts) {
    return <div>error</div>;
  }


  return (
    <div className={"flex flex-col justify-center items-center mt-4 space-y-6"}>
      {products.length === 0 ? (
        <p>Nie dodano żadnych produktów</p>
      ) : (
        products.map((item: {id: number, name: string, count: number}) => (
          <Card key={item.id} className="w-[600px]">
            <CardHeader>
              <CardTitle>{item.name} - {item.count} </CardTitle>
            </CardHeader>
          </Card>
        ))
      )}
    </div>
  );
}

const fetchProductsCount = async () => fetchData<{id: number, name: string, count: number}[]>("products/count/");