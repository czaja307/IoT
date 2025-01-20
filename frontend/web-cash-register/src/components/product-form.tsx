"use client";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { ProductProps } from "@/lib/types";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { useMutation, useQuery } from "@tanstack/react-query";
import { editData, fetchData } from "@/lib/api";
import { useRouter } from "next/navigation";

interface ProductFormProps {
    name: string,
    description: string,
    price: string,
}

function ProductForm({ productId = null }: { productId: number | null }) {
  const router = useRouter();
  const [errors, setErrors] = useState<Record<string, string>>({});

  const { data: product, isLoading: isLoadingProducts, isError: isErrorProducts } = useQuery({
    queryKey: ["product"],
    queryFn: () => fetchProduct(Number(productId)),
    enabled: !!productId
  });


  const [formData, setFormData] = useState({
    name: "",
    price: "",
    description: ""
  });

  useEffect(() => {
    if (productId) {
      if (product) {
        setFormData({
            name: product.name,
            price: product.price.toString(),
            description: product.description
          }
        );
      }
    }
  }, [product, productId]);

  const productMutation = useMutation({
    mutationFn: (data: ProductFormProps) => {
      const endpoint = productId ? `products/${productId}` : "products";
      const method = productId ? "PUT" : "POST";
      return editData(endpoint, method, { body: JSON.stringify(data) });
    },
    onSuccess: () => {
      alert(`Produkt ${productId ? "zaktualizowany" : "dodany"}`);
      router.push("/");
    },
    onError: async (error: any) => {
      if (error?.validationError) {
        setErrors(error.validationError);
      } else {
        alert(`Nie udało się ${productId ? "zaktualizować" : "dodać"}`);
      }
    }
  });


  if (isLoadingProducts) {
    return <div>loading...</div>;
  }

  if (isErrorProducts) {
    return <div>error</div>;
  }

  const handleChange = (e: { target: { name: any; value: any; }; }) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    setErrors((prevErrors) => ({ ...prevErrors, [name]: "" }));

  };

  const handleSubmit = (e: { preventDefault: () => void; }) => {
    e.preventDefault();

    if (!formData.name.trim() || !formData.price.trim() || !formData.description.trim()) {
      alert("All fields are required");
      return;
    }

    const payload = {
      name: formData.name,
      price: formData.price.toString(),
      description: formData.description
    };

    productMutation.mutate(payload);
  };

  return (
    <div>
      <div className={"flex justify-center items-center mt-4"}>
        <Card className="w-[650px]">
          <CardHeader>
            <CardTitle>{productId ? "Edytuj produkt" : "Dodaj produkt"}</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit}>
              <div className="flex flex-col space-y-1.5 m-4">
                <Label htmlFor="name">Nazwa</Label>
                <Input
                  id={"name"}
                  name={"name"}
                  value={formData.name}
                  type="text"
                  onChange={handleChange}
                  required={true}
                />
                {errors.name && <p className="text-red-600 text-sm">{errors.name}</p>}
              </div>
              <div className="flex flex-col space-y-1.5 m-4">
                <Label htmlFor="description">Opis</Label>
                <Input
                  id={"description"}
                  name={"description"}
                  value={formData.description}
                  type="text"
                  onChange={handleChange}
                  required={true}
                />
                {errors.description && <p className="text-red-600 text-sm">{errors.description}</p>}
              </div>
              <div className="flex flex-col space-y-1.5 m-4">
                <Label htmlFor="price">Cena</Label>
                <Input
                  id={"price"}
                  name={"price"}
                  value={formData.price}
                  type="number"
                  step={0.01}
                  onChange={handleChange}
                  required={true}
                />
                {errors.price && <p className="text-red-600 text-sm">{errors.price}</p>}
              </div>
            </form>
            <CardFooter>
              <Button onClick={handleSubmit} type="submit">
                Zapisz
              </Button>
            </CardFooter>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}


const fetchProduct = async (productId: number) => fetchData<ProductProps>(`products/${productId}`);


export { ProductForm };

